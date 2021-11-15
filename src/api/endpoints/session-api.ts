import {
  SessionModel,
  UserChangeModel,
  UserModel,
  UserResetModel,
} from "@/types";
import httpClient from "./http-client";
import { Endpoint, fillEndpoint } from "./endpoints";

const TEST_SESSION_EXISTING = false;

/**
 * Returns the current user's session.
 *
 * @return SessionModel - The session for the previously logged in user.
 *
 * @throws Error - If no session exists.
 */
export async function getSession(): Promise<SessionModel> {
  if (!TEST_SESSION_EXISTING) {
    throw Error("<No session should return a 400 which throws an error>");
  }

  return httpClient<SessionModel>(fillEndpoint(Endpoint.session), {
    method: "GET",
  });
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
  return httpClient<SessionModel>(fillEndpoint(Endpoint.createAccount), {
    method: "POST",
    body: JSON.stringify(user),
  });
}

/**
 * Logs the given user in.
 *
 * @param user - The user to log in.
 *
 * @return SessionModel - The session for the logged in user.
 *
 * @throws Error - If no session exists.
 */
export async function loginUser(user: UserModel): Promise<SessionModel> {
  return httpClient<SessionModel>(fillEndpoint(Endpoint.login), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}

/**
 * Logs the current user out.
 */
export async function logoutUser(): Promise<void> {
  await httpClient(fillEndpoint(Endpoint.logout), {
    method: "GET",
  });
}

/**
 * Requests to reset the password of the given user.
 *
 * @param user - The user to reset.
 */
export async function forgotPassword(user: UserResetModel): Promise<void> {
  await httpClient(fillEndpoint(Endpoint.forgotPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}

/**
 * Requests to change a user's password.
 *
 * @param user - The user to change the password.
 *
 * @throws Error - The password change request was unsuccessful.
 */
export async function changePassword(user: UserChangeModel): Promise<void> {
  await httpClient(fillEndpoint(Endpoint.changePassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}
