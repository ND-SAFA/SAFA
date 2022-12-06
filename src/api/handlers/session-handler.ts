// import { datadogRum } from "@datadog/browser-rum";

import {
  IOHandlerCallback,
  PasswordChangeSchema,
  UserPasswordSchema,
} from "@/types";
import { sessionStore, logStore } from "@/hooks";
import { getParam, getParams, navigateTo, QueryParams, Routes } from "@/router";
import {
  handleClearProject,
  createLoginSession,
  savePassword,
  deleteAccount,
  handleLoadLastProject,
  handleGetProjects,
  getCurrentUser,
} from "@/api";

/**
 * Attempts to log a user in.
 *
 * @param user - The user to log in.
 * @throws If login is unsuccessful.
 */
export async function handleLogin(user: UserPasswordSchema): Promise<void> {
  const session = await createLoginSession(user);
  const goToPath = getParam(QueryParams.LOGIN_PATH);
  const query = { ...getParams() };

  delete query[QueryParams.LOGIN_PATH];

  sessionStore.user = await getCurrentUser();
  sessionStore.updateSession(session);

  // datadogRum.startSessionReplayRecording();

  await handleGetProjects({
    onComplete: async () => {
      if (goToPath === Routes.ARTIFACT) {
        await handleLoadLastProject();
      } else if (typeof goToPath === "string") {
        await navigateTo(goToPath, query);
      } else {
        await navigateTo(Routes.HOME, query);
      }
    },
  });
}

/**
 * Logs a user out.
 */
export async function handleLogout(): Promise<void> {
  document.cookie = "";

  await handleClearProject();
  await navigateTo(Routes.LOGIN_ACCOUNT);
  sessionStore.clearSession();
  logStore.notifications = [];
  // await deleteSession();
  // datadogRum.startSessionReplayRecording();
}

/**
 * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
 * If the token does not, is expired, or is otherwise invalid, the user will be sent back to login.
 */
export async function handleAuthentication(): Promise<void> {
  sessionStore.user = await getCurrentUser();

  // datadogRum.init({
  //   applicationId: process.env.VUE_APP_DDOG_APP_ID || "",
  //   clientToken: process.env.VUE_APP_DDOG_DDOG_TOKEN || "",
  //   env: process.env.NODE_ENV || "",
  //   site: "datadoghq.com",
  //   service: "safa",
  //   version: "1.0.0",
  //   sampleRate: 100,
  //   premiumSampleRate: 100,
  //   trackInteractions: true,
  //   defaultPrivacyLevel: "mask-user-input",
  // });
  // datadogRum.startSessionReplayRecording();

  await handleGetProjects({});
}

/**
 * Updates a user's password.
 *
 * @param password - The old and new password.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleChangePassword(
  password: PasswordChangeSchema,
  { onSuccess, onError }: IOHandlerCallback
): void {
  savePassword(password)
    .then(() => {
      logStore.onSuccess("Your password has been updated.");
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError("Unable to update your password.");
      logStore.onDevError(e);
      onError?.(e);
    });
}

/**
 * Confirms and deletes a user's account.
 *
 * @param password - The user's current password.
 */
export function handleDeleteAccount(password: string): void {
  logStore.confirm(
    "Delete your account?",
    "This action cannot be undone.",
    async (isConfirmed) => {
      if (!isConfirmed) return;

      deleteAccount(password).then(handleLogout);
    }
  );
}
