import { createSession } from "@/util";
import { navigateTo, Routes } from "@/router";
import { deltaModule, sessionModule, subtreeModule } from "@/store";
import { loginUser } from "@/api/endpoints";
import { clearProject } from "./set-project-handler";
import { UserModel } from "@/types";
import { loadLastProject } from "@/api";

/**
 * Attempts to log a user in.
 */
export async function login(user: UserModel): Promise<void> {
  const session = await loginUser(user);

  sessionModule.SET_SESSION(session);
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
    } else if (isAuthorized && location.includes(Routes.ARTIFACT_TREE)) {
      await loadLastProject();
    }
  } catch (e) {
    await logout();
  }
}
