/**
 * Defines a user model.
 */
export interface UserModel {
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
}

/**
 * Defines a user model for password reset.
 */
export type UserResetModel = Omit<UserModel, "password">;

/**
 * Defines a user model for password updating.
 */
export interface UserChangeModel {
  /**
   * The token generated and included by email as a query param to securely change a user's password.
   */
  token: string;
  /**
   * The new password to set.
   */
  password: string;
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
