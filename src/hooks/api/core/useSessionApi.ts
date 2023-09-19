import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  IOHandlerCallback,
  PasswordChangeSchema,
  SessionApiHook,
  UserPasswordSchema,
} from "@/types";
import { DEMO_ACCOUNT } from "@/util";
import {
  getProjectApiStore,
  setProjectApiStore,
  sessionStore,
  logStore,
  permissionStore,
  getOrgApiStore,
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
 * A store for handling session API requests.
 */
export const useSessionApi = defineStore("sessionApi", (): SessionApiHook => {
  const createdAccount = ref(false);
  const passwordSubmitted = ref(false);
  const sessionApi = useApi("sessionApi")();
  const authApi = useApi("authApi")();

  const loading = computed(() => sessionApi.loading);
  const authLoading = computed(() => authApi.loading);
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

  function handleReset(): void {
    createdAccount.value = false;
    passwordSubmitted.value = false;
    sessionApi.handleReset();
  }

  async function handleCreateAccount(user: UserPasswordSchema): Promise<void> {
    await sessionApi.handleRequest(async () => {
      await createUser(user);

      createdAccount.value = true;
    });
  }

  async function handlePasswordReset(email: string): Promise<void> {
    await sessionApi.handleRequest(async () => {
      await createPasswordReset({ email });

      passwordSubmitted.value = true;
    });
  }

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

  async function handleLogin(user: UserPasswordSchema): Promise<void> {
    await sessionApi.handleRequest(async () => {
      const session = await createLoginSession(user);
      const goToPath = getParam(QueryParams.LOGIN_PATH);
      const query = { ...getParams() };

      delete query[QueryParams.LOGIN_PATH];

      sessionStore.user = await getCurrentUser();
      sessionStore.updateSession(session);

      await getProjectApiStore.handleReload({
        onComplete: async () => {
          await getOrgApiStore.handleLoadCurrent();

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

  async function handleDemoLogin(): Promise<void> {
    permissionStore.isDemo = true;

    await handleLogin(DEMO_ACCOUNT).then(() =>
      navigateTo(Routes.ARTIFACT, {
        [QueryParams.VERSION]: "cf354d4b-21d7-4f8e-8951-e447ddf77997",
      })
    );
  }

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

  async function handleAuthentication(
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await authApi.handleRequest(async () => {
      sessionStore.user = await getCurrentUser();

      if (sessionStore.user.email === DEMO_ACCOUNT.email) {
        permissionStore.isDemo = true;
      }

      await getOrgApiStore.handleLoadCurrent();
      await getProjectApiStore.handleReload({});
    }, callbacks);
  }

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
    authLoading,
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
