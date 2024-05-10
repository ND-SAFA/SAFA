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
  return buildRequest<SessionSchema>("accountCreate").sessionRequest({
    method: "POST",
    body: JSON.stringify(user),
  });
}

/**
 * Creates a new pre-verified account.
 *
 * @param user - The user to create.
 * @return The session for the logged in user.
 * @throws If the account cannot be created.
 */
export async function createVerifiedUser(
  user: UserPasswordSchema
): Promise<SessionSchema> {
  return buildRequest<SessionSchema, string, UserPasswordSchema>(
    "accountCreateVerified"
  ).post(user);
}

/**
 * Verifies a new account.
 *
 * @param token - The account token to verify.
 */
export async function saveUserVerification(token: string): Promise<void> {
  return buildRequest<void, string, { token: string }>(
    "accountVerify"
  ).sessionRequest(
    {
      method: "POST",
      body: JSON.stringify({ token }),
    },
    true
  );
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
  return buildRequest<UserSchema>("accountGet").get();
}

/**
 * Requests to reset the password of the given user.
 *
 * @param user - The user to reset.
 */
export async function createPasswordReset(
  user: UserResetSchema
): Promise<void> {
  await buildRequest<void, string, UserResetSchema>("accountForgot").put(user);
}

/**
 * Requests to reset the password of the given user.
 * - This is a special case for admin users.
 * - The reset email is not sent to the user, but to the admin.
 *
 * @param user - The user to reset.
 */
export async function createAdminPasswordReset(
  user: UserResetSchema
): Promise<void> {
  await buildRequest<void, string, UserResetSchema>("accountForgotAdmin").put(
    user
  );
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
  return buildRequest("accountReset").sessionRequest({
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
  await buildRequest<void, string, PasswordChangeSchema>("accountChange").put(
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
  await buildRequest<void, string, { password: string }>("accountDelete").post({
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
    "accountOrg"
  ).put({
    defaultOrgId,
  });
}
