import { defineStore } from "pinia";

import { GenerateArtifactSchema, IOHandlerCallback } from "@/types";
import { orgStore, projectStore, useApi } from "@/hooks";
import { createCheckoutSession, createCostEstimate } from "@/api";
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

  return { handleEstimateCost, handleCheckoutSession };
});

export default useBillingApi(pinia);
