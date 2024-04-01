import { defineStore } from "pinia";

import { CostEstimateSchema, JobSchema } from "@/types";
import {
  MAX_GENERATED_BASE_ARTIFACTS,
  ONBOARDING_MEET_LINK,
  ONBOARDING_STEPS,
  ONBOARDING_SUPPORT_LINK,
} from "@/util";
import {
  artifactStore,
  integrationsStore,
  jobStore,
  orgStore,
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
    /**
     * Whether generation should ignore current jobs.
     */
    ignoreCurrentJobs: false,
  }),
  getters: {
    /**
     * @return The onboarding project's upload job, if the generation step is done.
     */
    uploadedJob(): JobSchema | undefined {
      return this.ignoreCurrentJobs ? undefined : jobStore.jobs[0];
    },
    /**
     * @return Whether the onboarding project's upload job is uploading artifacts.
     */
    isUploadJob(): boolean {
      return (
        this.uploadedJob?.steps.includes("Retrieving Github Repository") ||
        false
      );
    },
    /**
     * @return Whether the onboarding project's upload job is generating artifacts.
     */
    isGenerationJob(): boolean {
      return this.uploadedJob?.steps.includes("Generating Artifacts") || false;
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
      const credits = this.cost?.credits;

      return (
        !orgStore.automaticBilling &&
        !this.paymentConfirmed &&
        !!credits &&
        orgStore.org.billing.monthlyRemainingCredits < credits
      );
    },
    /**
     * @return A display string for the onboarding project's upload job.
     */
    uploadProgress(): string {
      const { steps = [], currentStep = 0 } = this.uploadedJob || {};
      return this.uploadedJob
        ? `Step ${currentStep + 1} of ${steps.length}: ${steps[currentStep]}`
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
    /**
     * @return Whether the onboarding workflow should skip to the repo step.
     */
    skipToRepo(): boolean {
      return integrationsStore.validGitHubCredentials;
    },
    /**
     * @return Whether the onboarding workflow should skip to the upload step.
     */
    skipToGenerate(): boolean {
      return !!(
        this.projectId &&
        ((this.isUploadJob && this.uploadedJob?.status === "COMPLETED") ||
          this.isGenerationJob)
      );
    },
    /**
     * @return Whether the onboarding workflow should skip to the upload step.
     */
    skipToUpload(): boolean {
      return this.isUploadJob || this.skipToGenerate;
    },
  },
  actions: {
    /**
     * Updates whether the generation has been completed based on the state of any current generation jobs.
     */
    updateGenerationCompleted(): void {
      this.generationCompleted =
        this.generationCompleted ||
        (this.isGenerationJob && this.uploadedJob?.status === "COMPLETED");
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
  },
});

export default useOnboarding(pinia);
