import { defineStore } from "pinia";

import { CostEstimateSchema, JobSchema } from "@/types";
import {
  ARTIFACT_GENERATION_ONBOARDING,
  jobStatus,
  MAX_GENERATED_BASE_ARTIFACTS,
  ONBOARDING_MEET_LINK,
  ONBOARDING_STEPS,
  ONBOARDING_SUPPORT_LINK,
} from "@/util";
import {
  artifactGenerationApiStore,
  artifactStore,
  billingApiStore,
  createProjectApiStore,
  getVersionApiStore,
  gitHubApiStore,
  integrationsStore,
  jobApiStore,
  jobStore,
  logStore,
  orgStore,
  projectApiStore,
  projectStore,
} from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { pinia } from "@/plugins";

/** This store manages the state of the onboarding workflow. */
export const useOnboarding = defineStore("useOnboarding", {
  state: () => ({
    /** Whether the onboarding workflow is open. */
    open: false,
    /** Whether the onboarding workflow ran into an error. */
    error: false,
    /** Whether the onboarding workflow is loading. */
    loading: false,
    /** The ID of the project used in onboarding.  */
    projectId: null as string | null,
    /** The current step of the onboarding workflow, starting at 1. */
    step: 1,
    /** The steps of the onboarding workflow, with their completion status.  */
    steps: Object.values(ONBOARDING_STEPS).map((step) => ({
      ...step,
      done: false,
    })),
    /** The cost of generating the selected project data. */
    cost: null as CostEstimateSchema | null,
    /** Whether payment has been confirmed. */
    paymentConfirmed: false,
    /** Whether the generation step has been completed. */
    generationCompleted: false,
  }),
  getters: {
    /** @return The onboarding project's upload job, if the generation step is done. */
    uploadedJob(): JobSchema | undefined {
      return jobStore.jobs[0];
    },
    /** @return Whether the onboarding project's upload job is uploading artifacts. */
    isUploadJob(): boolean {
      return (
        this.uploadedJob?.steps.includes("Retrieving Github Repository") ||
        false
      );
    },
    /** @return Whether the onboarding project's upload job is generating artifacts. */
    isGenerationJob(): boolean {
      return this.uploadedJob?.steps.includes("Generating Artifacts") || false;
    },
    /** @return Whether the onboarding workflow should display the generated project overview. */
    displayProject(): boolean {
      return (
        this.step >= ONBOARDING_STEPS.summarize.number &&
        projectStore.isProjectDefined
      );
    },
    /** @return Whether the onboarding workflow should display billing information. */
    displayBilling(): boolean {
      const credits = this.cost?.credits;

      return (
        !orgStore.automaticBilling &&
        !this.paymentConfirmed &&
        !!credits &&
        orgStore.org.billing.monthlyRemainingCredits < credits
      );
    },
    /** @return A display string for the onboarding project's upload job. */
    uploadProgress(): string {
      const { steps = [], currentStep = 0 } = this.uploadedJob || {};
      return this.uploadedJob
        ? `Step ${currentStep + 1} of ${steps.length}: ${
            steps[currentStep]
          } (${jobStatus(this.uploadedJob).duration()})`
        : "";
    },
    /** @return Whether the onboarding workflow should block generation because of project size. */
    blockGeneration(): boolean {
      return (
        projectStore.isProjectDefined &&
        artifactStore.allArtifacts.length > MAX_GENERATED_BASE_ARTIFACTS
      );
    },
  },
  actions: {
    /**
     * Reloads the GitHub projects and jobs for the onboarding workflow.
     * @param open - Whether to force open the onboarding workflow.
     * @param reset - Whether to reset the project ID.
     */
    async handleReload(open?: boolean, reset?: boolean): Promise<void> {
      if (reset) {
        // Reset all onboarding state.
        this.projectId = null;
        this.open = true;
        this.step = 1;
        this.steps.forEach((step) => (step.done = false));
        await billingApiStore.handleUpdateOnboardingStatus({
          completed: false,
          projectId: "",
        });
      } else {
        // Load the current onboarding status.
        await billingApiStore.handleGetOnboardingStatus({
          onSuccess: (status) => {
            // Open the onboarding workflow if it has not yet been completed, or is manually opened.
            this.projectId = status.projectId || null;
            this.open = open || !status.completed;
          },
        });
      }

      // Skip reset if already loading or completed.
      if (!this.open || this.loading) return;

      this.loading = true;

      await gitHubApiStore.handleVerifyCredentials();
      await jobApiStore.handleReload();

      // Load the project ID and generation status based on stored state, job state, or local storage.
      this.generationCompleted =
        this.generationCompleted ||
        (this.isGenerationJob && this.uploadedJob?.status === "COMPLETED");
      const skipToGenerate =
        this.projectId &&
        ((this.isUploadJob && this.uploadedJob?.status === "COMPLETED") ||
          this.isGenerationJob);
      const skipToUpload = !reset && (this.isUploadJob || skipToGenerate);

      if (integrationsStore.validGitHubCredentials) {
        // Skip to Code step if credentials are set.
        await this.handleNextStep("connect");
      }
      if (skipToUpload) {
        // Skip to the Summarize step if a job has been started, or a project has already been uploaded.
        await this.handleNextStep("code");
      }
      if (skipToGenerate) {
        // Skip to the Generate step if a job has been completed.
        await this.handleNextStep("summarize");
      }

      this.loading = false;
    },
    /**
     * Close the popup and mark onboarding as complete.
     * @param resetProject - Whether to reset the project ID.
     * */
    async handleClose(resetProject?: boolean): Promise<void> {
      this.open = false;
      await billingApiStore.handleUpdateOnboardingStatus({
        completed: true,
        projectId: resetProject ? "" : this.projectId || "",
      });
    },
    /** Load the project for the onboarding workflow. */
    async loadProject(): Promise<void> {
      if (this.projectId) {
        await getVersionApiStore.handleLoadCurrent(
          { projectId: this.projectId },
          { onError: () => (this.projectId = "") }
        );
      } else if (this.uploadedJob?.completedEntityId) {
        await getVersionApiStore.handleLoad(
          this.uploadedJob?.completedEntityId
        );
      }
    },
    /**
     * Proceeds to the next step of the onboarding workflow.
     * @param currentStep - The current step. If not provided, proceeds to the next step.
     */
    async handleNextStep(
      currentStep?: keyof typeof ONBOARDING_STEPS
    ): Promise<void> {
      const index = currentStep
        ? ONBOARDING_STEPS[currentStep].index
        : this.step - 1;

      this.steps[index].done = true;
      this.steps[index + 1].done = true;

      if (this.step === index + 1) {
        this.step = index + 2;
      }

      if (currentStep === "connect") {
        integrationsStore.validGitHubCredentials = true;
        await gitHubApiStore.handleLoadProjects();
      }

      if (currentStep === "summarize") {
        await this.loadProject();
        await this.handleEstimateCost();
      }
    },
    /**
     * Schedule a call with the SAFA team.
     * @param error - Whether the call was scheduled because of an error.
     */
    handleScheduleCall(error: boolean): void {
      window.open(
        error ? ONBOARDING_SUPPORT_LINK : ONBOARDING_MEET_LINK,
        "_blank"
      );
    },
    /** Import from GitHub and summarize project files. */
    async handleImportProject(): Promise<void> {
      integrationsStore.gitHubConfig.summarize = true;
      await createProjectApiStore.handleGitHubImport({
        onSuccess: () => jobApiStore.handleReload(),
        onError: () => (this.error = true),
      });
    },
    /**
     * Calculate the cost of generating the selected project data.
     * Skipped if billing information is not displayed.
     */
    async handleEstimateCost(): Promise<void> {
      await billingApiStore.handleEstimateCost(
        {
          artifacts: artifactStore.allArtifacts.map(({ id }) => id),
          targetTypes: ARTIFACT_GENERATION_ONBOARDING,
        },
        {
          onSuccess: (cost) => (this.cost = cost),
          onError: () => (this.error = true),
        }
      );
    },
    /**
     * Generate documentation for the selected project.
     * @param paymentConfirmed - Whether the user has confirmed payment.
     */
    async handleGenerateDocumentation(
      paymentConfirmed?: boolean
    ): Promise<void> {
      const credits = this.cost?.credits;
      this.paymentConfirmed = paymentConfirmed || false;

      if (!credits) {
        this.error = true;
        return;
      }

      if (this.displayBilling) {
        await billingApiStore.handleCheckoutSession(
          this.cost?.credits || 0,
          `Artifact Generation: ${projectStore.project.name}`
        );
      } else {
        await artifactGenerationApiStore.handleGenerateArtifacts(
          {
            artifacts: artifactStore.allArtifacts.map(({ id }) => id),
            targetTypes: ARTIFACT_GENERATION_ONBOARDING,
          },
          { onError: () => (this.error = true) }
        );
      }
    },
    /** Export the selected project as a CSV. */
    async handleExportProject() {
      await this.loadProject();
      await projectApiStore.handleDownload("csv");
      logStore.onSuccess("Your data is being exported.");
      await this.handleClose(true);
    },
    /** View the selected project in SAFA */
    async handleViewProject() {
      await this.loadProject();
      await navigateTo(Routes.ARTIFACT, { projectId: this.projectId });
      await this.handleClose(true);
    },
  },
});

export default useOnboarding(pinia);
