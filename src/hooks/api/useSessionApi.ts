import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  IOHandlerCallback,
  PasswordChangeSchema,
  UserPasswordSchema,
} from "@/types";
import { getParam, getParams, navigateTo, QueryParams, Routes } from "@/router";
import {
  handleClearProject,
  createLoginSession,
  savePassword,
  deleteAccount,
  handleLoadLastProject,
  handleGetProjects,
  getCurrentUser,
  deleteSession,
  createUser,
  createPasswordReset,
  updatePassword,
} from "@/api";
import { sessionStore, logStore } from "@/hooks/core";
import { pinia } from "@/plugins";
import { useApi } from "@/hooks/api/useApi";

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

      delete query[QueryParams.LOGIN_PATH];

      sessionStore.user = await getCurrentUser();
      sessionStore.updateSession(session);

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
    });
  }

  /**
   * Logs a user out to the login screen.
   *
   * @param sendLogoutRequest - Whether to send the API request to log out.
   */
  async function handleLogout(sendLogoutRequest = false): Promise<void> {
    document.cookie = "";

    await handleClearProject();
    await navigateTo(Routes.LOGIN_ACCOUNT);
    sessionStore.clearSession();
    logStore.notifications = [];

    if (sendLogoutRequest) {
      await deleteSession();
    }
  }

  /**
   * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
   * @throws If the authentication token is invalid.
   */
  async function handleAuthentication(): Promise<void> {
    sessionStore.user = await getCurrentUser();

    await handleGetProjects({});
  }

  /**
   * Updates a user's password.
   *
   * @param password - The old and new password.
   * @param callbacks - The callbacks to run on success or error.
   */
  function handleChangePassword(
    password: PasswordChangeSchema,
    callbacks: IOHandlerCallback
  ): void {
    sessionApi.handleRequest(() => savePassword(password), callbacks, {
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

        await sessionApi.handleRequest(
          () => deleteAccount(password),
          {
            onSuccess: () => handleLogout(),
          },
          { error: "Unable to delete your account." }
        );
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
    handleLogout,
    handleAuthentication,
    handleChangePassword,
    handleDeleteAccount,
  };
});

export default useSessionApi(pinia);
