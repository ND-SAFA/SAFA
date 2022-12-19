/**
 * Defines an artifact warning.
 */
export interface WarningSchema {
  /**
   * The artifact rule name.
   */
  ruleName: string;
  /**
   * The artifact rule message.
   */
  ruleMessage: string;
}

/**
 * A collection of warnings keyed by artifact id.
 */
export type WarningCollectionSchema = Record<string, WarningSchema[]>;
