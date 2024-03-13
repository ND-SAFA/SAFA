import { defineStore } from "pinia";

import {
  BillingApiHook,
  CostEstimateSchema,
  GenerateArtifactSchema,
  IOHandlerCallback,
  OnboardingStatusSchema,
} from "@/types";
import { onboardingStore, orgStore, projectStore, useApi } from "@/hooks";
import {
  createCheckoutSession,
  createCostEstimate,
  deleteCheckoutSession,
  getOnboardingStatus,
  setOnboardingStatus,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * This store manages interactions with the billing API.
 */
export const useBillingApi = defineStore("billingApi", (): BillingApiHook => {
  const billingApi = useApi("billingApi");

  async function handleGetOnboardingStatus(
    callbacks: IOHandlerCallback<OnboardingStatusSchema>
  ): Promise<void> {
    await billingApi.handleRequest(() => getOnboardingStatus(), callbacks);
  }

  async function handleUpdateOnboardingStatus(
    status: OnboardingStatusSchema
  ): Promise<void> {
    await billingApi.handleRequest(() => setOnboardingStatus(status));
  }

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
    await onboardingStore.handleReload(true);
    await onboardingStore.handleGenerateDocumentation(true);
  }

  async function handleCancelPayment(sessionId: string): Promise<void> {
    await billingApi.handleRequest(() => deleteCheckoutSession(sessionId));
  }

  return {
    handleGetOnboardingStatus,
    handleUpdateOnboardingStatus,
    handleEstimateCost,
    handleCheckoutSession,
    handleAcceptPayment,
    handleCancelPayment,
  };
});

export default useBillingApi(pinia);
