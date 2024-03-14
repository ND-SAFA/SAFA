import { OnboardingStatusSchema } from "@/types";
import { ONBOARDING_STEPS } from "@/util";

/**
 * A hook for calling onboarding API endpoints.
 */
export interface OnboardingApiHook {
  /**
   * Gets the onboarding status for the current user.
   * @param open - Whether to open the onboarding workflow regardless of its status.
   */
  handleGetOnboardingStatus(open?: boolean): Promise<void>;
  /**
   * Gets the onboarding status for the current user.
   * @param status - The new onboarding status.
   */
  handleUpdateOnboardingStatus(status: OnboardingStatusSchema): Promise<void>;
  /**
   * Closes the onboarding modal and marks the workflow as completed.
   * - The onboarding workflow will no longer open on startup, unless reset.
   *
   * @param openTo - If set, onboarding project ID will be reset.
   *                     - "export" - The project will be downloaded.
   *                     - "view" - The project will be opened in the graph.
   * */
  handleCloseOnboarding(openTo?: "export" | "view"): Promise<void>;
  /**
   * Opens the onboarding workflow and marks the workflow as incomplete.
   * - The onboarding workflow will be reset to start on the first step.
   * */
  handleOpenOnboarding(): Promise<void>;
  /**
   * Imports the current GitHub project configuration,
   * and generates summaries for the project.
   */
  handleImportAndSummarize(): Promise<void>;
  /**
   * Loads the given project, and estimates the cost of generating documentation for it.
   * @param projectId - The ID of the project to estimate the cost for.
   */
  handleEstimateCost(projectId: string): Promise<void>;
  /**
   * Generate documentation for the selected project.
   * @param paymentConfirmed - Whether the user has confirmed payment.
   */
  handleGenerateDocumentation(paymentConfirmed?: boolean): Promise<void>;

  /**
   Proceeds to the next step of the onboarding workflow.
   - If the current step is "connect", reload projects from GitHub.
   - If the current step is "summarize" and a project ID can be found,
     estimate the cost of generation.
   @param currentStep - The current step. If not provided, proceeds to the next step.
   */
  handleLoadNextStep(
    currentStep?: keyof typeof ONBOARDING_STEPS
  ): Promise<void>;
  /**
   * Loads all state related to the onboarding workflow.
   * - Depending on the step of completion, other state such as jobs and projects may be loaded.
   * - If this workflow is already loading, it will not be reloaded.
   *
   * @param updateState - Whether to update the onboarding state.
   *                    - "open" - Open the onboarding workflow regardless.
   *                    - "reset" - Reset the onboarding workflow to the beginning.
   */
  handleLoadOnboardingState(updateState?: "open" | "reset"): Promise<void>;
}
