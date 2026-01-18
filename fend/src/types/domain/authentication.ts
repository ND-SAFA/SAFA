/**
 * Defines a user model.
 */
export interface UserSchema {
  /**
   * The user's id.
   */
  userId: string;
  /**
   * The user's email.
   */
  email: string;
  /**
   * The id of this user's personal organization.
   */
  personalOrgId: string;
  /**
   * The id of this user's current default organization.
   */
  defaultOrgId: string;
  /**
   * Whether this user is a superuser.
   */
  superuser: boolean;
  /**
   * If the user is a superuser, whether they are in superuser mode.
   */
  admin?: { active: boolean };
}

/**
 * Defines a user & password model.
 */
export interface UserPasswordSchema {
  /**
   * The user's email.
   */
  email: string;
  /**
   * The user's password.
   */
  password: string;
}

/**
 * Defines a session model.
 */
export interface SessionSchema {
  /**
   * The JWT token authorizing current user.
   */
  token: string;
  /**
   * The version ID to load when the app loads.
   */
  versionId?: string;
}

/**
 * Defines a user model for password reset.
 */
export interface UserResetSchema {
  /**
   * The user's email.
   */
  email: string;
}

/**
 * Defines a user model for password reset.
 */
export interface PasswordResetSchema {
  /**
   * The token generated and included by email as a query param to securely change a user's password.
   */
  resetToken: string;
  /**
   * The new password to set.
   */
  newPassword: string;
}

/**
 * Defines a user model for password change.
 */
export interface PasswordChangeSchema {
  /**
   * The current password to change.
   */
  oldPassword: string;
  /**
   * The new password to set.
   */
  newPassword: string;
}

/**
 * Defines a user API keys model.
 */
export interface UserApiKeysSchema {
  /**
   * The user's OpenAI API key (masked on retrieval).
   */
  openaiApiKey?: string;
  /**
   * The user's Anthropic API key (masked on retrieval).
   */
  anthropicApiKey?: string;
  /**
   * The user's preferred LLM provider.
   */
  preferredProvider?: 'openai' | 'anthropic';
}

/**
 * LLM Provider options.
 */
export type LLMProvider = 'openai' | 'anthropic';

/**
 * LLM Provider display information.
 */
export interface LLMProviderOption {
  value: LLMProvider;
  label: string;
  description: string;
}
