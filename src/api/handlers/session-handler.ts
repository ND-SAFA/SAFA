import { createSession } from "@/util";
import { navigateTo, Routes } from "@/router";
import { deltaModule, sessionModule, subtreeModule } from "@/store";
import { loginUser } from "@/api/endpoints";
import { clearProject } from "./set-project-handler";
import { UserModel } from "@/types";

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
  await sessionModule.SET_SESSION(createSession());
  await clearProject();
  await subtreeModule.clearSubtrees();
  deltaModule.clearDelta();
  await navigateTo(Routes.LOGIN_ACCOUNT);
}
