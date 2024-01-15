import { defineStore } from "pinia";

import { JobSchema, LocalStorageKeys } from "@/types";
import {
  ARTIFACT_GENERATION_TYPES,
  MAX_GENERATED_BASE_ARTIFACTS,
  ONBOARDING_STEPS,
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
  onboardingStore,
  orgStore,
  projectApiStore,
  projectStore,
} from "@/hooks";
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
     * The types of artifacts that will be generated.
     */
    generationTypes: [
      ARTIFACT_GENERATION_TYPES.FUNCTIONAL_REQ,
      ARTIFACT_GENERATION_TYPES.FEATURE,
    ],
    /**
     * The cost of generating the selected project data.
     */
    cost: null as number | null,
    /**
     * Whether payment has been confirmed.
     */
    paymentConfirmed: false,
  }),
  getters: {
    /**
     * @return Whether the onboarding workflow is complete.
     */
    isComplete(): boolean {
      return localStorage.getItem(LocalStorageKeys.onboarding) === "true";
    },
    /**
     * @return The onboarding project's upload job, if the generation step is done.
     */
    uploadedJob(): JobSchema | undefined {
      return jobStore.jobs[0];
    },
    /**
     * @return Whether the onboarding workflow should display the generated project overview.
     */
    displayProject(): boolean {
      return (
        this.step >= ONBOARDING_STEPS.summarize.number &&
        projectStore.isProjectDefined
      );
    },
    /**
     * @return Whether the onboarding workflow should display billing information.
     */
    displayBilling(): boolean {
      return !orgStore.automaticBilling && !this.paymentConfirmed;
    },
    /**
     * @return A display string for the onboarding project's upload job.
     */
    uploadProgress(): string {
      return this.uploadedJob
        ? `Step ${this.uploadedJob.currentStep + 1} of ${
            this.uploadedJob.steps.length
          }: ${this.uploadedJob.steps[this.uploadedJob.currentStep]}`
        : "";
    },
    /**
     * @return Whether the onboarding workflow should block generation because of project size.
     */
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
     */
    async handleReload(open?: boolean): Promise<void> {
      if (open) {
        this.open = true;
      } else if (onboardingStore.isComplete) {
        return;
      }

      if (this.loading) return; // Skip reset if already loading.

      this.loading = true;

      await gitHubApiStore.handleVerifyCredentials();
      await jobApiStore.handleReload();

      // Move from Connect GitHub step if credentials are set.
      if (integrationsStore.validGitHubCredentials) {
        await onboardingStore.handleNextStep("connect");
      }
      // Skip to the Summarize step if a job has been uploaded.
      if (onboardingStore.uploadedJob) {
        await onboardingStore.handleNextStep("code");
      }
      // Skip to the Generate step if a job has been completed.
      if (onboardingStore.uploadedJob?.completedEntityId) {
        await onboardingStore.handleNextStep("summarize");
      }

      this.loading = false;
    },
    /**
     * Close the popup and mark onboarding as complete.
     */
    handleClose(): void {
      this.open = false;
      localStorage.setItem(LocalStorageKeys.onboarding, "true");
    },
    /**
     * Proceeds to the next step of the onboarding workflow.
     * @param step - The step to proceed to. If not provided, proceeds to the next step.
     */
    async handleNextStep(step?: keyof typeof ONBOARDING_STEPS): Promise<void> {
      const index = step ? ONBOARDING_STEPS[step].index : this.step - 1;

      this.steps[index].done = true;
      this.steps[index + 1].done = true;

      if (this.step === index + 1) {
        this.step = index + 2;
      }

      if (step === "connect") {
        await gitHubApiStore.handleLoadProjects();
      }

      if (step === "summarize" && this.uploadedJob?.completedEntityId) {
        await getVersionApiStore
          .handleLoad(this.uploadedJob?.completedEntityId, undefined, false)
          .then(() => this.handleEstimateCost());
      }
    },
    /**
     * Schedule a call with the SAFA team.
     */
    handleScheduleCall(): void {
      // TODO
    },
    /**
     * Import from GitHub and summarize project files.
     */
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
          targetTypes: this.generationTypes,
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
      this.paymentConfirmed = paymentConfirmed || false;

      const artifactIds = artifactStore.allArtifacts.map(({ id }) => id);

      if (this.displayBilling && !paymentConfirmed) {
        await billingApiStore.handleCheckoutSession(artifactIds.length);
      } else {
        await artifactGenerationApiStore.handleGenerateArtifacts(
          {
            artifacts: artifactIds,
            targetTypes: this.generationTypes,
          },
          {
            onError: () => (this.error = true),
          }
        );
      }
    },
    /**
     * Export the selected project as a CSV.
     */
    async handleExportProject() {
      if (!this.uploadedJob?.completedEntityId) return;

      await getVersionApiStore.handleLoad(this.uploadedJob?.completedEntityId);
      await projectApiStore.handleDownload("csv");

      logStore.onSuccess("Your data is being exported.");

      this.handleClose();
    },
    /**
     * View the selected project in SAFA.
     */
    async handleViewProject() {
      if (!this.uploadedJob?.completedEntityId) return;

      await getVersionApiStore.handleLoad(this.uploadedJob?.completedEntityId);

      this.handleClose();
    },
  },
});

export default useOnboarding(pinia);
