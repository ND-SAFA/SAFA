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
export type SessionModel = Omit<UserModel, "password">;

/**
 * Defines a user model for password reset.
 */
export type UserResetModel = Omit<UserModel, "password">;

/**
 * Defines a user model for password updating.
 */
export interface UserChangeModel extends UserModel {
  /**
   * The token generated and included by email as a query param to securely change a user's password.
   */
  token: string;
}
