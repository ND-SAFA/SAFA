import {
  CostEstimateSchema,
  GenerateArtifactSchema,
  IOHandlerCallback,
  OnboardingStatusSchema,
} from "@/types";

/**
 * A hook for calling billing API endpoints.
 */
export interface BillingApiHook {
  /**
   * Gets the onboarding status for the current user.
   * @param callbacks - The callbacks for the action, with the onboarding status as the payload.
   */
  handleGetOnboardingStatus(
    callbacks: IOHandlerCallback<OnboardingStatusSchema>
  ): Promise<void>;
  /**
   * Gets the onboarding status for the current user.
   * @param status - The new onboarding status.
   */
  handleUpdateOnboardingStatus(status: OnboardingStatusSchema): Promise<void>;
  /**
   * Estimates the cost of generating artifacts.
   *
   * @param configuration - The configuration for generating the artifacts.
   * @param callbacks - The callbacks for the action.
   * @return The estimated cost of generating the artifacts, in dollars.
   */
  handleEstimateCost(
    configuration: GenerateArtifactSchema,
    callbacks: IOHandlerCallback<CostEstimateSchema>
  ): Promise<void>;
  /**
   * Creates a new checkout session to add credits.
   * @param amount - The amount of credits to buy.
   * @param description - The description of the transaction.
   */
  handleCheckoutSession(amount: number, description: string): Promise<void>;
  /**
   * Accepts the payment for the checkout session.
   * Internally, the BE will still ensure that the
   * user has enough credits to generate.
   */
  handleAcceptPayment(): Promise<void>;
  /**
   * Cancels the payment for the checkout session.
   * @param sessionId - The id of the session to cancel.
   */
  handleCancelPayment(sessionId: string): Promise<void>;
}
