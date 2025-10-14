import {
  CostEstimateSchema,
  GenerateArtifactSchema,
  OnboardingStatusSchema,
  OrgPaymentTier,
  PurchaseDetailsSchema,
  TransactionSchema,
  UpdatePaymentTierSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Gets the onboarding status for the current user.
 * @returns The onboarding status.
 */
export function getOnboardingStatus(): Promise<OnboardingStatusSchema> {
  return buildRequest<OnboardingStatusSchema>("onboardingStatus").get();
}

/**
 * Sets the onboarding status for the current user.
 * @param status - The new onboarding status.
 * @returns The updated onboarding status.
 */
export function setOnboardingStatus(
  status: OnboardingStatusSchema
): Promise<OnboardingStatusSchema> {
  return buildRequest<OnboardingStatusSchema, string, OnboardingStatusSchema>(
    "onboardingStatus"
  ).put(status);
}

/**
 * Estimates the cost of generating parent artifacts from child artifacts.
 *
 * @param config - The configuration for generating the artifacts.
 * @param versionId - The version to estimate generation for.
 * @returns An estimate of the cost to generate the artifacts, in dollars.
 */
export function createCostEstimate(
  config: GenerateArtifactSchema,
  versionId: string
): Promise<CostEstimateSchema> {
  return buildRequest<CostEstimateSchema, "versionId", GenerateArtifactSchema>(
    "billingEstimate",
    { versionId }
  ).post(config);
}

/**
 * Creates a checkout session for purchasing data generation.
 * @param paymentDetails - The details of the payment.
 * @returns The transaction details for the purchase.
 */
export function createCheckoutSession(
  paymentDetails: PurchaseDetailsSchema
): Promise<TransactionSchema> {
  return buildRequest<TransactionSchema, string, PurchaseDetailsSchema>(
    "billingCheckout"
  ).post(paymentDetails);
}

/**
 * Deletes a checkout session.
 * @param sessionId - The id of the session to delete.
 */
export function deleteCheckoutSession(sessionId: string): Promise<void> {
  return buildRequest<void, "sessionId", void>("billingCheckoutDelete", {
    sessionId,
  }).post();
}

/**
 * Updates the payment tier of an organization.
 * @param organizationId - The organization to update.
 * @param tier - The new payment tier.
 */
export function setOrgPaymentTier(
  organizationId: string,
  tier: OrgPaymentTier
): Promise<void> {
  return buildRequest<void, string, UpdatePaymentTierSchema>("billingTier").put(
    {
      organizationId,
      tier,
    }
  );
}

/**
 * Returns all transactions for an organization.
 * @param orgId - The organization to get transactions for.
 */
export function getAllBillingTransactions(
  orgId: string
): Promise<TransactionSchema[]> {
  return buildRequest<TransactionSchema[], "orgId">("transactions", {
    orgId,
  }).get();
}

/**
 * Returns all transactions for an organization, or the current month.
 * @param orgId - The organization to get transactions for.
 */
export function getMonthlyBillingTransactions(
  orgId: string
): Promise<TransactionSchema[]> {
  return buildRequest<TransactionSchema[], "orgId">("transactionsMonthly", {
    orgId,
  }).get();
}
