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
   *
   * @action Updates onboarding to no longer open on startup.
   *
   * @param openTo - If set, onboarding project ID will be reset.
   *               - "export" - The project will be downloaded.
   *               - "view" - The project will be opened in the graph.
   * */
  handleCloseOnboarding(openTo?: "export" | "view"): Promise<void>;
  /**
   * Opens the onboarding workflow and resets all onboarding state.
   *
   * @action Resets all onboarding state to the first step.
   * @action Ignores current onboarding jobs, to allow the user to start a new import.
   * @action Updates onboarding to open on startup.
   * */
  handleOpenOnboarding(): Promise<void>;
  /**
   * Imports the current GitHub project configuration and generates project summaries.
   *
   * @assumption The integrations store contains a valid GitHub import configuration.
   * @action After importing, reloads current jobs and stops ignoring onboarding jobs.
   */
  handleImportAndSummarize(): Promise<void>;
  /**
   * Loads the given project, and estimates the cost of generating documentation for it.
   *
   * @action Loads the onboarding project, either from a saved project ID, or the version ID from the last uploaded job.
   */
  handleEstimateCost(): Promise<void>;
  /**
   * Generate documentation for the selected project.
   *
   * @assumption The project has been loaded and is ready for generation.
   * @assuption The estimated cost of generation has already been calculated.
   * @action If the user needs to pay, opens the payment portal.
   * @action If the user does not need to pay, generates artifacts.
   */
  handleGenerateDocumentation(): Promise<void>;
  /**
   * Proceeds to the next step of the onboarding workflow.
   *
   * @action If the current step is "connect", reload projects from GitHub.
   * @action If the current step is "summarize",estimate the cost of generation.
   * @action Update the step in the onboarding store.
   *
   * @param currentStep - The current step. If not provided, proceeds to the next step.
   */
  handleLoadNextStep(
    currentStep?: keyof typeof ONBOARDING_STEPS
  ): Promise<void>;
  /**
   * Loads all state related to the onboarding workflow.
   * - Depending on the step of completion, other state such as jobs and projects may be loaded.
   * - If this workflow is already loading, it will not be reloaded.
   *
   * @condition If the user is in demo mode, or onboarding is already open or loading,
   *            the onboarding state will not be loaded.
   * @action Depending on "updateState", the onboarding state may be reset or loaded from the server.
   * @action Loads GitHub credentials, jobs, and updates whether onboarding has already been generated.
   * @action If GitHub has credentials, moves to the "code" step.
   * @action If a job has been started, or a project has already been uploaded, moves to the "summarize" step.
   * @action If a summarize job has been completed, or generation job exists, moves to the "generate" step.
   *
   * @param updateState - Whether to update the onboarding state.
   *                    - "open" - Open the onboarding workflow regardless.
   *                    - "reset" - Reset the onboarding workflow to the beginning.
   */
  handleLoadOnboardingState(updateState?: "open" | "reset"): Promise<void>;
}
