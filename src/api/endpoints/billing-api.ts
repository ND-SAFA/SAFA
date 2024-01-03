import {
  CostEstimateSchema,
  GenerateArtifactSchema,
  PurchaseDetailsSchema,
  TransactionSchema,
} from "@/types";
import { buildRequest } from "@/api";

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
    "createCostEstimate",
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
    "createCheckoutSession"
  ).post(paymentDetails);
}

/**
 * Deletes a checkout session.
 * @param sessionId - The id of the session to delete.
 */
export function deleteCheckoutSession(sessionId: string): Promise<void> {
  return buildRequest<void, "sessionId", void>("deleteCheckoutSession", {
    sessionId,
  }).post();
}
