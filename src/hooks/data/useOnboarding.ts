import { defineStore } from "pinia";

import { CostEstimateSchema, JobSchema, LocalStorageKeys } from "@/types";
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

/**
 * This store manages the state of the onboarding workflow.
 */
export const useOnboarding = defineStore("useOnboarding", {
  state: () => ({
    /**
     * Whether the onboarding workflow is open.
     */
    open: false,
    /**
     * Whether the onboarding workflow ran into an error.
     */
    error: false,
    /**
     * Whether the onboarding workflow is loading.
     */
    loading: false,
    /**
     * The ID of the project used in onboarding.
     */
    projectId: null as string | null,
    /**
     * The current step of the onboarding workflow, starting at 1.
     */
    step: 1,
    /**
     * The steps of the onboarding workflow, with their completion status.
     */
    steps: Object.values(ONBOARDING_STEPS).map((step) => ({
      ...step,
      done: false,
    })),
    /**
     * The cost of generating the selected project data.
     */
    cost: null as CostEstimateSchema | null,
    /**
     * Whether payment has been confirmed.
     */
    paymentConfirmed: false,
    /**
     * Whether the generation step has been completed.
     */
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
      return !orgStore.automaticBilling && !this.paymentConfirmed;
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
     */
    async handleReload(open?: boolean): Promise<void> {
      // Open the onboarding workflow if it has not yet been completed, or is manually opened.
      if (
        open ||
        (localStorage.getItem(LocalStorageKeys.onboarding) !== "true" &&
          projectStore.allProjects.length <= 1)
      ) {
        this.open = true;
      } else return;

      // Skip reset if already loading.
      if (this.loading) return;

      this.loading = true;

      await gitHubApiStore.handleVerifyCredentials();
      await jobApiStore.handleReload();

      // Load the project ID and generation status based on stored state, job state, or local storage.
      this.projectId =
        this.projectId ||
        (this.isUploadJob && this.uploadedJob?.completedEntityId) ||
        localStorage.getItem(LocalStorageKeys.onboardingProject);
      this.generationCompleted =
        this.generationCompleted ||
        (this.isGenerationJob && this.uploadedJob?.status === "COMPLETED") ||
        localStorage.getItem(LocalStorageKeys.onboardingGenerated) === "true";

      if (integrationsStore.validGitHubCredentials) {
        // Skip to Code step if credentials are set.
        await this.handleNextStep("connect");
      }
      if (this.isUploadJob || this.projectId) {
        // Skip to the Summarize step if a job has been uploaded, or a project has been stored.
        await this.handleNextStep("code");
      }
      if (this.projectId) {
        // Skip to the Generate step if a job has been completed.
        await this.handleNextStep("summarize");
      }
      if (this.generationCompleted) {
        // Skip to everything completed if the generation is complete.
        await this.handleNextStep("generate");
      }

      this.loading = false;
    },
    /** Close the popup and mark onboarding as complete. */
    handleClose(): void {
      this.open = false;
      localStorage.setItem(LocalStorageKeys.onboarding, "true");
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
      const projectId = this.projectId || this.uploadedJob?.completedEntityId;

      if (currentStep === "generate") {
        this.generationCompleted = true;
        localStorage.setItem(LocalStorageKeys.onboardingGenerated, "true");

        return;
      }

      this.steps[index].done = true;
      this.steps[index + 1].done = true;

      if (this.step === index + 1) {
        this.step = index + 2;
      }

      if (currentStep === "connect") {
        await gitHubApiStore.handleLoadProjects();
      }

      if (currentStep === "summarize" && projectId) {
        await getVersionApiStore.handleLoad(projectId, undefined, false, {
          onSuccess: () => {
            this.projectId = projectId;
            localStorage.setItem(LocalStorageKeys.onboardingProject, projectId);
            this.handleEstimateCost();
          },
          onError: () => {
            this.projectId = "";
            localStorage.setItem(LocalStorageKeys.onboardingProject, "");
          },
        });
      }
    },
    /**
     * Schedule a call with the SAFA team.
     * @param error - Whether the call was scheduled because of an error.
     */
    handleScheduleCall(error: boolean): void {
      window.open(error ? ONBOARDING_SUPPORT_LINK : ONBOARDING_MEET_LINK);
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
      if (!this.displayBilling) return;

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
      const artifactIds = artifactStore.allArtifacts.map(({ id }) => id);
      this.paymentConfirmed = paymentConfirmed || false;

      if (this.displayBilling && !paymentConfirmed) {
        await billingApiStore.handleCheckoutSession(artifactIds.length);
      } else {
        await artifactGenerationApiStore.handleGenerateArtifacts(
          {
            artifacts: artifactIds,
            targetTypes: ARTIFACT_GENERATION_ONBOARDING,
          },
          { onError: () => (this.error = true) }
        );
      }
    },
    /** Export the selected project as a CSV. */
    async handleExportProject() {
      await projectApiStore.handleDownload("csv");
      logStore.onSuccess("Your data is being exported.");
      this.handleClose();
    },
    /** View the selected project in SAFA */
    async handleViewProject() {
      await navigateTo(Routes.ARTIFACT, { projectId: this.projectId });
      this.handleClose();
    },
  },
});

export default useOnboarding(pinia);
