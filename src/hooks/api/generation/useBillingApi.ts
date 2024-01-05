import { defineStore } from "pinia";

import { GenerateArtifactSchema, IOHandlerCallback } from "@/types";
import { onboardingStore, orgStore, projectStore, useApi } from "@/hooks";
import {
  createCheckoutSession,
  createCostEstimate,
  deleteCheckoutSession,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * This store manages interactions with the billing API.
 */
export const useBillingApi = defineStore("billingApi", () => {
  const billingApi = useApi("billingApi");

  /**
   * Estimates the cost of generating artifacts.
   *
   * @param configuration - The configuration for generating the artifacts.
   * @param callbacks - The callbacks for the action.
   * @return The estimated cost of generating the artifacts, in dollars.
   */
  async function handleEstimateCost(
    configuration: GenerateArtifactSchema,
    callbacks: IOHandlerCallback<number>
  ): Promise<void> {
    await billingApi.handleRequest(
      async () =>
        (await createCostEstimate(configuration, projectStore.versionId)).cost,
      callbacks
    );
  }

  /**
   * Creates a new checkout session to add credits.
   * @param amount - The amount of credits to buy.
   */
  async function handleCheckoutSession(amount: number): Promise<void> {
    await billingApi.handleRequest(async () => {
      const transaction = await createCheckoutSession({
        organizationId: orgStore.orgId,
        amount,
        description: "Artifact Generation",
      });

      window.open(transaction.redirectUrl);
    });
  }

  /**
   * Accepts the payment for the checkout session.
   * Internally, the BE will still ensure that the
   * user has enough credits to generate.
   */
  async function handleAcceptPayment(): Promise<void> {
    await onboardingStore.handleReload(true);
    await onboardingStore.handleGenerateDocumentation(true);
  }

  /**
   * Cancels the payment for the checkout session.
   * @param sessionId - The id of the session to cancel.
   */
  async function handleCancelPayment(sessionId: string): Promise<void> {
    await billingApi.handleRequest(() => deleteCheckoutSession(sessionId));
  }

  return {
    handleEstimateCost,
    handleCheckoutSession,
    handleAcceptPayment,
    handleCancelPayment,
  };
});

export default useBillingApi(pinia);
