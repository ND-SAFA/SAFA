import { UserModel } from "@/types";
import { createSession } from "@/util";
import { getParam, getParams, navigateTo, QueryParams, Routes } from "@/router";
import { sessionModule } from "@/store";
import {
  handleLoadLastProject,
  handleClearProject,
  createLoginSession,
} from "@/api";

/**
 * Attempts to log a user in.
 *
 * @param user - The user to log in.
 */
export async function handleLogin(user: UserModel): Promise<void> {
  const session = await createLoginSession(user);
  const goToPath = getParam(QueryParams.LOGIN_PATH);
  const query = { ...getParams() };

  delete query[QueryParams.LOGIN_PATH];

  sessionModule.SET_SESSION(session);

  if (typeof goToPath === "string" && goToPath !== Routes.ARTIFACT) {
    await navigateTo(goToPath, query);
  } else {
    await navigateTo(Routes.ARTIFACT, query);
    await handleLoadLastProject();
  }
}

/**
 * Logs a user out.
 */
export async function handleLogout(): Promise<void> {
  sessionModule.SET_SESSION(createSession());
  await navigateTo(Routes.LOGIN_ACCOUNT);
  await handleClearProject();
}

/**
 * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
 * If the token does not, is expired, or is otherwise invalid, the user will be sent back to login.
 */
export async function handleAuthentication(): Promise<void> {
  try {
    const isAuthorized = await sessionModule.hasAuthorization();
    const location = window.location.href;

    if (!isAuthorized) {
      await handleLogout();
    } else if (isAuthorized && location.includes(Routes.ARTIFACT)) {
      await handleLoadLastProject();
    }
  } catch (e) {
    await handleLogout();
  }
}
