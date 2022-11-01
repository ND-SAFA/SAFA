/**
 * Defines a user model.
 */
export interface UserModel {
  /**
   * The user's id.
   */
  userId: string;
  /**
   * The user's email.
   */
  email: string;
}

/**
 * Defines a user & password model.
 */
export interface UserPasswordModel {
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
export interface SessionModel {
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
export interface UserResetModel {
  /**
   * The user's email.
   */
  email: string;
}

/**
 * Defines a user model for password reset.
 */
export interface PasswordResetModel {
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
export interface PasswordChangeModel {
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
 * Defines the decoded object of an authorization JWT token
 */
export interface AuthToken {
  /**
   * The identifier (email) of the subscriber.
   */
  sub: string;
  /**
   * Expiration date in number of seconds since epoch.
   */
  exp: number;
}
