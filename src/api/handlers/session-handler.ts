import {
  ConfirmationType,
  IOHandlerCallback,
  PasswordChangeModel,
  UserModel,
} from "@/types";
import { sessionStore, logStore } from "@/hooks";
import {
  getParam,
  getParams,
  navigateTo,
  QueryParams,
  router,
  Routes,
  routesPublic,
} from "@/router";
import {
  handleClearProject,
  createLoginSession,
  savePassword,
  deleteAccount,
  handleLoadLastProject,
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

  sessionStore.updateSession(session);

  if (goToPath === Routes.ARTIFACT) {
    await handleLoadLastProject();
  } else if (typeof goToPath === "string") {
    await navigateTo(goToPath, query);
  } else {
    await navigateTo(Routes.HOME, query);
  }
}

/**
 * Logs a user out.
 */
export async function handleLogout(): Promise<void> {
  await handleClearProject();
  await navigateTo(Routes.LOGIN_ACCOUNT);
  sessionStore.clearSession();
}

/**
 * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
 * If the token does not, is expired, or is otherwise invalid, the user will be sent back to login.
 */
export async function handleAuthentication(): Promise<void> {
  if (routesPublic.includes(router.currentRoute.path)) return;

  try {
    const isAuthorized = await sessionStore.hasAuthorization;

    if (isAuthorized) return;

    await handleLogout();
  } catch (e) {
    await handleLogout();
  }
}

/**
 * Updates a user's password.
 *
 * @param password - The old and new password.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleChangePassword(
  password: PasswordChangeModel,
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
  logStore.$patch({
    confirmation: {
      type: ConfirmationType.INFO,
      title: `Delete your account?`,
      body: `This action cannot be undone.`,
      statusCallback: (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        deleteAccount(password).then(handleLogout);
      },
    },
  });
}
