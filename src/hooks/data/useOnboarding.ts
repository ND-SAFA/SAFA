import { defineStore } from "pinia";

import { JobSchema, LocalStorageKeys } from "@/types";
import { ARTIFACT_GENERATION_TYPES, ONBOARDING_STEPS } from "@/util";
import {
  createProjectApiStore,
  getVersionApiStore,
  gitHubApiStore,
  integrationsStore,
  jobApiStore,
  jobStore,
  logStore,
  onboardingStore,
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
     * The current step of the onboarding workflow, starting at 1.
     */
    step: 1,
    /**
     * The steps of the onboarding workflow, with their completion status.
     */
    steps: Object.values(ONBOARDING_STEPS).map((step) => ({
      ...step,
      done: true,
    })),
    /**
     * The types of artifacts that will be generated.
     */
    generationTypes: [
      ARTIFACT_GENERATION_TYPES.FUNCTIONAL_REQ,
      ARTIFACT_GENERATION_TYPES.FEATURE,
    ],
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
        this.step === ONBOARDING_STEPS.generate.number &&
        projectStore.isProjectDefined
      );
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

      if (integrationsStore.validGitHubCredentials) {
        await gitHubApiStore.handleLoadProjects();
      }

      await jobApiStore.handleReload();
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
    handleNextStep(step?: keyof typeof ONBOARDING_STEPS): void {
      const index = step ? ONBOARDING_STEPS[step].index : this.step - 1;

      this.steps[index].done = true;

      if (this.step === index + 1) {
        this.step = index + 2;
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
     * Generate documentation for the selected project.
     */
    async handleGenerateDocumentation(): Promise<void> {
      // TODO
    },
    /**
     * Export the selected project as a CSV.
     */
    async handleExportProject() {
      if (!this.uploadedJob?.completedEntityId) return;

      await getVersionApiStore.handleLoadCurrent({
        projectId: this.uploadedJob.completedEntityId,
      });

      await projectApiStore.handleDownload(
        "csv",
        this.uploadedJob.completedEntityId
      );

      logStore.onSuccess("Your data is being exported.");
      this.handleClose();
    },
    /**
     * View the selected project in SAFA.
     */
    async handleViewProject() {
      if (!this.uploadedJob?.completedEntityId) return;

      await getVersionApiStore.handleLoadCurrent({
        projectId: this.uploadedJob.completedEntityId,
      });

      this.handleClose();
    },
  },
});

export default useOnboarding(pinia);
