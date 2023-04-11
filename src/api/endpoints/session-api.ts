import {
  SessionSchema,
  PasswordResetSchema,
  UserPasswordSchema,
  UserResetSchema,
  PasswordChangeSchema,
  UserSchema,
} from "@/types";
import { baseURL, Endpoint, fillEndpoint, authHttpClient } from "@/api";

/**
 * Custom fetch call for session endpoints.
 *
 * @param args - Args to pass to fetch.
 * @throws Error - Response status was not 200.
 */
async function sessionFetch<T>(...args: Parameters<typeof fetch>): Promise<T> {
  const response = await fetch(`${baseURL}/${args[0]}`, {
    ...args[1],
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw Error("Unable to find a session.");
  }

  return response.json();
}

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
  return sessionFetch<SessionSchema>(fillEndpoint(Endpoint.createAccount), {
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
  return sessionFetch<SessionSchema>(fillEndpoint(Endpoint.login), {
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
  return authHttpClient<UserSchema>(fillEndpoint(Endpoint.getAccount), {
    method: "GET",
  });
}

/**
 * Requests to reset the password of the given user.
 *
 * @param user - The user to reset.
 */
export async function createPasswordReset(
  user: UserResetSchema
): Promise<void> {
  await authHttpClient(fillEndpoint(Endpoint.forgotPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
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
  await sessionFetch(fillEndpoint(Endpoint.resetPassword), {
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
  await authHttpClient(fillEndpoint(Endpoint.updatePassword), {
    method: "PUT",
    body: JSON.stringify(password),
  });
}

/**
 * Requests to delete a user's account.
 *
 * @param password - The current password.
 * @throws The delete request was unsuccessful.
 */
export async function deleteAccount(password: string): Promise<void> {
  await authHttpClient(fillEndpoint(Endpoint.deleteAccount), {
    method: "POST",
    body: JSON.stringify({ password }),
  });
}

/**
 * Logs out the current user.
 */
export async function deleteSession(): Promise<void> {
  await authHttpClient(fillEndpoint(Endpoint.logout), {
    method: "GET",
  }).catch(() => {
    // TODO: this should not be failing.
  });
}
