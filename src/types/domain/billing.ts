/**
 * Represents an estimation of the cost of generating data.
 */
export interface CostEstimateSchema {
  /**
   * The estimated cost of generating, in dollars.
   */
  cost: number;
}

/**
 * Represents the details of a purchase.
 */
export interface PurchaseDetailsSchema {
  /**
   * The id of the organization to purchase for.
   */
  organizationId: string;
  /**
   * The amount of credits to buy.
   */
  amount: number;
  /**
   * The description of the payment.
   */
  description: string;
}

/**
 * Represents the details of a transaction to pay for data generation.
 */
export interface TransactionSchema {
  /**
   * The id of the transaction.
   */
  id: string;
  /**
   * The status of the transaction.
   */
  status: string;
  /**
   The amount of credits to buy.
   */
  amount: number;
  /**
   * The description of the payment.
   */
  description: string;
  /**
   * The timestamp of the transaction.
   */
  timestamp: string;
  /**
   * The payment url to redirect to after the transaction is created.
   */
  redirectUrl: string;
}
