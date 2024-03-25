import { defineStore } from "pinia";

import {
  BillingApiHook,
  CostEstimateSchema,
  GenerateArtifactSchema,
  IOHandlerCallback,
} from "@/types";
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
export const useBillingApi = defineStore("billingApi", (): BillingApiHook => {
  const billingApi = useApi("billingApi");

  async function handleEstimateCost(
    configuration: GenerateArtifactSchema,
    callbacks: IOHandlerCallback<CostEstimateSchema>
  ): Promise<void> {
    await billingApi.handleRequest(
      async () =>
        await createCostEstimate(configuration, projectStore.versionId),
      callbacks
    );
  }

  async function handleCheckoutSession(
    amount: number,
    description: string
  ): Promise<void> {
    await billingApi.handleRequest(async () => {
      const transaction = await createCheckoutSession({
        organizationId: orgStore.orgId,
        amount,
        description,
      });

      window.open(transaction.redirectUrl);
    });
  }

  async function handleAcceptPayment(): Promise<void> {
    onboardingStore.paymentConfirmed = true;
  }

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
