import { UserModel } from "@/types";
import { createSession } from "@/util";
import { getParam, getParams, navigateTo, QueryParams, Routes } from "@/router";
import { deltaModule, sessionModule, subtreeModule } from "@/store";
import { loadLastProject, clearProject, loginUser } from "@/api";

/**
 * Attempts to log a user in.
 */
export async function login(user: UserModel): Promise<void> {
  const session = await loginUser(user);
  const goToPath = getParam(QueryParams.LOGIN_PATH);
  const query = { ...getParams() };

  delete query[QueryParams.LOGIN_PATH];

  sessionModule.SET_SESSION(session);

  if (typeof goToPath === "string" && goToPath !== Routes.ARTIFACT) {
    await navigateTo(goToPath, query);
  } else {
    await navigateTo(Routes.ARTIFACT, query);
    await loadLastProject();
  }
}

/**
 * Attempts to log a user out.
 */
export async function logout(): Promise<void> {
  sessionModule.SET_SESSION(createSession());
  await navigateTo(Routes.LOGIN_ACCOUNT);
  deltaModule.clearDelta();
  await subtreeModule.clearSubtrees();
  await clearProject();
}

/**
 * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
 * If the token does not, is expired, or is otherwise invalid, the user will be sent back to login.
 */
export async function verifyAuthentication(): Promise<void> {
  try {
    const isAuthorized = await sessionModule.hasAuthorization();
    const location = window.location.href;

    if (!isAuthorized) {
      await logout();
    } else if (isAuthorized && location.includes(Routes.ARTIFACT)) {
      await loadLastProject();
    }
  } catch (e) {
    await logout();
  }
}
