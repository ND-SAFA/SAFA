import {
  APIOptions,
  SessionModel,
  UserChangeModel,
  UserModel,
  UserResetModel,
} from "@/types";
import httpClient from "./http-client";
import { baseURL, Endpoint, fillEndpoint } from "./endpoints";
import { sessionModule } from "@/store";

/**
 * TODO: remove once endpoints exist.
 */
const TEST_ENDPOINTS = true;
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

  if (TEST_ENDPOINTS) {
    return { email: "123@example.com" };
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
  return httpClient<SessionModel>(
    fillEndpoint(Endpoint.createAccount),
    {
      method: "POST",
      body: JSON.stringify(user),
    },
    true,
    false
  );
}

/**
 * Logs the given user in and stores authorization token in the current session.
 *
 * @param user - The user to log in.
 *
 * @return SessionModel - The session for the logged in user.
 *
 * @throws Error - If no session exists.
 */
export async function loginUser(user: UserModel): Promise<SessionModel> {
  return new Promise((resolve, reject) => {
    const endpoint = `${baseURL}/${fillEndpoint(Endpoint.login)}`;
    const options: APIOptions = {
      method: "POST",
      body: JSON.stringify(user),
    };
    fetch(endpoint, options)
      .then((res) => {
        if (res.status !== 200) return reject("Login failed.");
        return res.json();
      })
      .then((resJson) => {
        const token = resJson.token;
        if (token === undefined)
          return reject("Response does not include authorization token");
        const session: SessionModel = {
          email: user.email,
          token: resJson.token,
        };
        resolve(session);
      })
      .catch(reject);
  });
}

/**
 * Logs the current user out.
 */
export async function logoutUser(): Promise<void> {
  if (TEST_ENDPOINTS) {
    return;
  }

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
  if (TEST_ENDPOINTS) {
    return;
  }

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
 * @return SessionModel - The session for the logged in user.
 *
 * @throws Error - The password change request was unsuccessful.
 */
export async function resetPassword(user: UserChangeModel): Promise<void> {
  if (TEST_ENDPOINTS) {
    return;
  }

  await httpClient<SessionModel>(fillEndpoint(Endpoint.resetPassword), {
    method: "PUT",
    body: JSON.stringify(user),
  });
}
