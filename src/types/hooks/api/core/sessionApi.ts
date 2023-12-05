import { ComputedRef, Ref } from "vue";
import {
  IOHandlerCallback,
  PasswordChangeSchema,
  UserPasswordSchema,
} from "@/types";

/**
 * A hook for managing the user session API.
 */
export interface SessionApiHook {
  /**
   * Whether this request manager is loading a request.
   */
  loading: ComputedRef<boolean>;
  /**
   * Whether the user's recently used account is being checked.
   */
  authLoading: ComputedRef<boolean>;
  /**
   * Whether the most recent request had an error.
   */
  error: ComputedRef<boolean>;
  /**
   * Whether a new account was created.
   */
  createdAccount: Ref<boolean>;
  /**
   * Whether a password change was submitted.
   */
  passwordSubmitted: Ref<boolean>;

  /**
   * An error message for account creation.
   */
  createErrorMessage: ComputedRef<string | false>;
  /**
   * An error message for password changes.
   */
  passwordErrorMessage: ComputedRef<string | false>;
  /**
   * An error message for login.
   */
  loginErrorMessage: ComputedRef<string | false>;

  /**
   * Resets the session API state.
   */
  handleReset(): void;
  /**
   * Attempts to verify a new account, using a token in the URL query.
   */
  handleVerifyAccount(token: string): Promise<void>;
  /**
   * Attempts to create a new account.
   *
   * @param user - The user to create.
   * @param verified - Whether the account is pre-verified.
   */
  handleCreateAccount(
    user: UserPasswordSchema,
    verified?: boolean
  ): Promise<void>;
  /**
   * Attempts to send a password reset email.
   *
   * @param email - The email to send the reset to.
   */
  handlePasswordReset(email: string): Promise<void>;
  /**
   * Attempts to reset a user's password.
   *
   * @param newPassword - The password and token to reset with.
   * @param resetToken - The token to reset with.
   */
  handlePasswordUpdate(newPassword: string, resetToken: string): Promise<void>;
  /**
   * Attempts to log a user in.
   *
   * @param user - The user to log in.
   */
  handleLogin(user: UserPasswordSchema): Promise<void>;
  /**
   * Logs in to the demo account and opens the demo project.
   */
  handleDemoLogin(): Promise<void>;
  /**
   * Logs a user out to the login screen.
   *
   * @param sendLogoutRequest - Whether to send the API request to log out.
   */
  handleLogout(sendLogoutRequest?: boolean): Promise<void>;
  /**
   * Verifies the stored authentication token,
   * and loads the last project if routing to the artifact tree.
   *
   * @param callbacks - The callbacks to run on success or error.
   */
  handleAuthentication(callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Updates a user's password.
   *
   * @param password - The old and new password.
   * @param callbacks - The callbacks to run on success or error.
   */
  handleChangePassword(
    password: PasswordChangeSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Confirms and deletes a user's account.
   *
   * @param password - The user's current password.
   */
  handleDeleteAccount(password: string): void;
}
