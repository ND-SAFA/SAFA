import {
  SessionModel,
  UserChangeModel,
  UserModel,
  UserResetModel,
} from "@/types";
import { baseURL, Endpoint, fillEndpoint, authHttpClient } from "@/api";

/**
 * Custom fetch call for session endpoints.
 *
 * @param args - Args to pass to fetch.
 * @throws Error - Response status was not 200.
 */
async function sessionFetch<T>(...args: Parameters<typeof fetch>): Promise<T> {
  const response = await fetch(`${baseURL}/${args[0]}`, args[1]);

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
export async function createUser(user: UserModel): Promise<SessionModel> {
  return sessionFetch<SessionModel>(fillEndpoint(Endpoint.createAccount), {
    method: "POST",
    body: JSON.stringify(user),
    headers: {
      "Content-Type": "application/json",
    },
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
  user: UserModel
): Promise<SessionModel> {
  return sessionFetch<SessionModel>(fillEndpoint(Endpoint.login), {
    method: "POST",
    body: JSON.stringify(user),
  });
}

/**
 * Requests to reset the password of the given user.
 *
 * @param user - The user to reset.
 */
export async function createPasswordReset(user: UserResetModel): Promise<void> {
  await authHttpClient(fillEndpoint(Endpoint.forgotPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}

/**
 * Requests to change a user's password.
 *
 * @param user - The user to change the password.
 * @throws The password change request was unsuccessful.
 */
export async function updatePassword(user: UserChangeModel): Promise<void> {
  await authHttpClient<SessionModel>(fillEndpoint(Endpoint.resetPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}
