/**
 * The props for the integrations stepper.
 */
export interface IntegrationsStepperProps {
  /**
   * Whether this stepper is to create a project or connect with an existing one.
   */
  type: "create" | "connect";
}

/**
 * The props for the integrations stepper.
 */
export interface AuthenticationListItemProps {
  /**
   * The name of the integration.
   */
  title: string;
  /**
   * Whether the user has credentials for this integration.
   */
  hasCredentials: boolean;
  /**
   * Whether this integration is loading.
   */
  loading?: boolean;
  /**
   * Whether this integration is disabled.
   */
  inactive?: boolean;
}
