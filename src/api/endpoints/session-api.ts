import {
  SessionModel,
  UserChangeModel,
  UserModel,
  UserResetModel,
} from "@/types";
import authHttpClient from "./auth-http-client";
import { baseURL, Endpoint, fillEndpoint } from "./endpoints";

/**
 * TODO: remove once endpoints exist.
 */

const TEST_ENDPOINTS = true;

/**
 * Custom fetch call for session endpoints.
 *
 * @param args - Args to pass to fetch.
 *
 * @throws Error - Response status was not 200.
 */
async function sessionFetch<T>(...args: Parameters<typeof fetch>): Promise<T> {
  const response = await fetch(...args);

  if (!response.ok) {
    throw Error("Unable to find a session.");
  }

  return response.json();
}

/**
 * Creates a new account.
 *
 * @param user - The user to create.
 *
 * @return SessionModel - The session for the logged in user.
 *
 * @throws Error - If the account cannot be created.
 */
export async function createUser(user: UserModel): Promise<SessionModel> {
  return sessionFetch<SessionModel>(
    `${baseURL}/${fillEndpoint(Endpoint.createAccount)}`,
    {
      method: "POST",
      body: JSON.stringify(user),
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
}

/**
 * Logs the given user in and stores authorization token in the current session.
 * This function uses the core fetch because it needs to intercept the HttpStatus
 * to validate if the call failed or succeeded.
 *
 * @param user - The user to log in.
 *
 * @return SessionModel - The session for the logged in user.
 *
 * @throws Error - If no session exists.
 */
export async function loginUser(user: UserModel): Promise<SessionModel> {
  return sessionFetch<SessionModel>(
    `${baseURL}/${fillEndpoint(Endpoint.login)}`,
    {
      method: "POST",
      body: JSON.stringify(user),
    }
  );
}

/**
 * Logs the current user out.
 */
export async function logoutUser(): Promise<void> {
  if (TEST_ENDPOINTS) {
    return;
  }

  await authHttpClient(fillEndpoint(Endpoint.logout), {
    method: "GET",
  });
}

/**
 * Requests to reset the password of the given user.
 *
 * @param user - The user to reset.
 */
export async function forgotPassword(user: UserResetModel): Promise<void> {
  if (TEST_ENDPOINTS) {
    return;
  }

  await authHttpClient(fillEndpoint(Endpoint.forgotPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}

/**
 * Requests to change a user's password.
 *
 * @param user - The user to change the password.
 *
 * @return SessionModel - The session for the logged in user.
 *
 * @throws Error - The password change request was unsuccessful.
 */
export async function resetPassword(user: UserChangeModel): Promise<void> {
  if (TEST_ENDPOINTS) {
    return;
  }

  await authHttpClient<SessionModel>(fillEndpoint(Endpoint.resetPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}
