import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  IOHandlerCallback,
  PasswordChangeSchema,
  UserPasswordSchema,
} from "@/types";
import { DEMO_ACCOUNT } from "@/util";
import {
  getProjectApiStore,
  setProjectApiStore,
  sessionStore,
  logStore,
  permissionStore,
} from "@/hooks";
import { getParam, getParams, navigateTo, QueryParams, Routes } from "@/router";
import {
  createLoginSession,
  savePassword,
  deleteAccount,
  getCurrentUser,
  deleteSession,
  createUser,
  createPasswordReset,
  updatePassword,
} from "@/api";
import { pinia } from "@/plugins";
import { useApi } from "@/hooks/api/core/useApi";

/**
 * Creates a store for handling session API requests.
 */
export const useSessionApi = defineStore("sessionApi", () => {
  const createdAccount = ref(false);
  const passwordSubmitted = ref(false);
  const sessionApi = useApi("sessionApi")();

  const loading = computed(() => sessionApi.loading);
  const error = computed(() => sessionApi.error);

  const loginErrorMessage = sessionApi.errorMessage(
    "Invalid username or password."
  );

  const createErrorMessage = sessionApi.errorMessage(
    "Unable to create an account."
  );

  const passwordErrorMessage = sessionApi.errorMessage(
    "Unable to update password."
  );

  /**
   * Resets the session API state.
   */
  function handleReset(): void {
    createdAccount.value = false;
    passwordSubmitted.value = false;
    sessionApi.handleReset();
  }

  /**
   * Attempts to create a new account.
   *
   * @param user - The user to create.
   */
  async function handleCreateAccount(user: UserPasswordSchema): Promise<void> {
    await sessionApi.handleRequest(async () => {
      await createUser(user);

      createdAccount.value = true;
    });
  }

  /**
   * Attempts to send a password reset email.
   *
   * @param email - The email to send the reset to.
   */
  async function handlePasswordReset(email: string): Promise<void> {
    await sessionApi.handleRequest(async () => {
      await createPasswordReset({ email });

      passwordSubmitted.value = true;
    });
  }

  /**
   * Attempts to reset a user's password.
   *
   * @param newPassword - The password and token to reset with.
   * @param resetToken - The token to reset with.
   */
  async function handlePasswordUpdate(
    newPassword: string,
    resetToken: string
  ): Promise<void> {
    await sessionApi.handleRequest(async () => {
      await updatePassword({
        newPassword,
        resetToken,
      });

      passwordSubmitted.value = true;
    });
  }

  /**
   * Attempts to log a user in.
   *
   * @param user - The user to log in.
   */
  async function handleLogin(user: UserPasswordSchema): Promise<void> {
    await sessionApi.handleRequest(async () => {
      const session = await createLoginSession(user);
      const goToPath = getParam(QueryParams.LOGIN_PATH);
      const query = { ...getParams() };

      console.log({ goToPath, query });

      delete query[QueryParams.LOGIN_PATH];

      sessionStore.user = await getCurrentUser();
      sessionStore.updateSession(session);

      await getProjectApiStore.handleReload({
        onComplete: async () => {
          if (goToPath === Routes.ARTIFACT) {
            await getProjectApiStore.handleLoadRecent();
          } else if (typeof goToPath === "string") {
            await navigateTo(goToPath, query);
          } else {
            await navigateTo(Routes.HOME, query);
          }
        },
      });
    });
  }

  /**
   * Logs in to the demo account and opens the demo project.
   */
  async function handleDemoLogin(): Promise<void> {
    permissionStore.isDemo = true;

    await handleLogin(DEMO_ACCOUNT).then(() =>
      navigateTo(Routes.ARTIFACT, {
        [QueryParams.VERSION]: "cf354d4b-21d7-4f8e-8951-e447ddf77997",
      })
    );
  }

  /**
   * Logs a user out to the login screen.
   *
   * @param sendLogoutRequest - Whether to send the API request to log out.
   */
  async function handleLogout(sendLogoutRequest = false): Promise<void> {
    await sessionApi.handleRequest(async () => {
      document.cookie = "";

      await setProjectApiStore.handleClear();
      await navigateTo(Routes.LOGIN_ACCOUNT);
      sessionStore.clearSession();
      logStore.notifications = [];

      if (sendLogoutRequest) {
        await deleteSession();
      }
    });
  }

  /**
   * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
   * @throws If the authentication token is invalid.
   */
  async function handleAuthentication(): Promise<void> {
    sessionStore.user = await getCurrentUser();

    if (sessionStore.user.email === DEMO_ACCOUNT.email) {
      permissionStore.isDemo = true;
    }

    await getProjectApiStore.handleReload({});
  }

  /**
   * Updates a user's password.
   *
   * @param password - The old and new password.
   * @param callbacks - The callbacks to run on success or error.
   */
  async function handleChangePassword(
    password: PasswordChangeSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await sessionApi.handleRequest(() => savePassword(password), {
      ...callbacks,
      success: "Your password has been updated.",
      error: "Unable to update your password.",
    });
  }

  /**
   * Confirms and deletes a user's account.
   *
   * @param password - The user's current password.
   */
  function handleDeleteAccount(password: string): void {
    logStore.confirm(
      "Delete your account?",
      "This action cannot be undone.",
      async (isConfirmed) => {
        if (!isConfirmed) return;

        await sessionApi.handleRequest(() => deleteAccount(password), {
          onSuccess: () => handleLogout(),
          error: "Unable to delete your account.",
        });
      }
    );
  }

  return {
    loading,
    error,
    createdAccount,
    passwordSubmitted,
    createErrorMessage,
    passwordErrorMessage,
    loginErrorMessage,
    handleReset,
    handleCreateAccount,
    handlePasswordReset,
    handlePasswordUpdate,
    handleLogin,
    handleDemoLogin,
    handleLogout,
    handleAuthentication,
    handleChangePassword,
    handleDeleteAccount,
  };
});

export default useSessionApi(pinia);
