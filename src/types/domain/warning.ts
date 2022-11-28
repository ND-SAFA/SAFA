/**
 * Defines an artifact warning.
 */
export interface WarningModel {
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
 * A collection of warnings for all artifacts.
 */
export type ProjectWarnings = Record<string, WarningModel[]>;
