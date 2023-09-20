import {
  SessionSchema,
  PasswordResetSchema,
  UserPasswordSchema,
  UserResetSchema,
  PasswordChangeSchema,
  UserSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates a new account.
 *
 * @param user - The user to create.
 * @return The session for the logged in user.
 * @throws If the account cannot be created.
 */
export async function createUser(
  user: UserPasswordSchema
): Promise<SessionSchema> {
  return buildRequest<SessionSchema>("createAccount").sessionRequest({
    method: "POST",
    body: JSON.stringify(user),
  });
}

/**
 * Logs the given user in.
 *
 * @param user - The user to log in.
 * @return The session for the logged in user.
 * @throws If no session exists.
 */
export async function createLoginSession(
  user: UserPasswordSchema
): Promise<SessionSchema> {
  return buildRequest<SessionSchema>("login").sessionRequest({
    method: "POST",
    body: JSON.stringify(user),
  });
}

/**
 * Gets the currently logged in user.
 *
 * @return The current user.
 * @throws If no user exists.
 */
export async function getCurrentUser(): Promise<UserSchema> {
  return buildRequest<UserSchema>("getAccount").get();
}

/**
 * Requests to reset the password of the given user.
 *
 * @param user - The user to reset.
 */
export async function createPasswordReset(
  user: UserResetSchema
): Promise<void> {
  await buildRequest<void, string, UserResetSchema>("forgotPassword").put(user);
}

/**
 * Requests to update a user's reset password.
 *
 * @param password - The password change information.
 * @throws The password change request was unsuccessful.
 */
export async function updatePassword(
  password: PasswordResetSchema
): Promise<void> {
  return buildRequest("resetPassword").sessionRequest({
    method: "PUT",
    body: JSON.stringify(password),
  });
}

/**
 * Requests to change a user's password.
 *
 * @param password - The password change information.
 * @throws The password change request was unsuccessful.
 */
export async function savePassword(
  password: PasswordChangeSchema
): Promise<void> {
  await buildRequest<void, string, PasswordChangeSchema>("updatePassword").put(
    password
  );
}

/**
 * Requests to delete a user's account.
 *
 * @param password - The current password.
 * @throws The delete request was unsuccessful.
 */
export async function deleteAccount(password: string): Promise<void> {
  await buildRequest<void, string, { password: string }>("deleteAccount").post({
    password,
  });
}

/**
 * Logs out the current user.
 */
export async function deleteSession(): Promise<void> {
  await buildRequest("logout").get().catch();
}

/**
 * Updates the user's default organization.
 *
 * @param defaultOrgId - The organization to set as the default.
 */
export async function saveDefaultOrg(defaultOrgId: string): Promise<void> {
  await buildRequest<void, string, Pick<UserSchema, "defaultOrgId">>(
    "editAccountOrg"
  ).put({
    defaultOrgId,
  });
}
