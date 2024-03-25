import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  IOHandlerCallback,
  PasswordChangeSchema,
  SessionApiHook,
  UserPasswordSchema,
} from "@/types";
import { DEMO_ACCOUNT, DEMO_VERSION_ID } from "@/util";
import {
  getOrgApiStore,
  getProjectApiStore,
  integrationsStore,
  logStore,
  onboardingApiStore,
  permissionStore,
  sessionStore,
  setProjectApiStore,
} from "@/hooks";
import {
  getParam,
  getParams,
  navigateTo,
  QueryParams,
  Routes,
  updateParam,
} from "@/router";
import {
  createLoginSession,
  createPasswordReset,
  createUser,
  createVerifiedUser,
  deleteAccount,
  deleteSession,
  getCurrentUser,
  savePassword,
  saveUserVerification,
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

  async function loadSessionData(): Promise<void> {
    permissionStore.isDemo = sessionStore.user.email === DEMO_ACCOUNT.email;

    await getOrgApiStore.handleLoadCurrent();
    await onboardingApiStore.handleLoadOnboardingState();
    await getProjectApiStore.handleLoadProjects();
  }

  function handleReset(): void {
    createdAccount.value = false;
    passwordSubmitted.value = false;
    sessionApi.handleReset();
  }

  async function handleCreateAccount(
    user: UserPasswordSchema,
    verified?: boolean
  ): Promise<void> {
    await sessionApi.handleRequest(
      async () => {
        if (verified) {
          await createVerifiedUser(user);
        } else {
          await createUser(user);
        }

        createdAccount.value = true;
      },
      {
        success: "Your account has been created.",
        error: "Unable to create your account.",
      }
    );
  }

  async function handleVerifyAccount(token: string): Promise<void> {
    await sessionApi.handleRequest(
      async () => {
        await saveUserVerification(token);
      },
      {
        success: "Your account has been verified.",
        error: "Unable to verify your account.",
      }
    );
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

      await loadSessionData();

      if (goToPath === Routes.ARTIFACT) {
        await getProjectApiStore.handleLoadRecent();
      } else if (typeof goToPath === "string") {
        await navigateTo(goToPath, query);
      } else {
        await navigateTo(Routes.HOME, query);
      }
    });
  }

  async function handleDemoLogin(): Promise<void> {
    await updateParam(
      QueryParams.VERSION,
      String(getParam(QueryParams.VERSION) || DEMO_VERSION_ID)
    );
    await updateParam(QueryParams.LOGIN_PATH, Routes.ARTIFACT, true);
    await handleLogin(DEMO_ACCOUNT);
  }

  async function handleLogout(
    sendLogoutRequest = false,
    createAccount?: boolean
  ): Promise<void> {
    await sessionApi.handleRequest(async () => {
      document.cookie = "";
      logStore.notifications = [];

      await setProjectApiStore.handleClear();
      integrationsStore.handleReset();
      sessionStore.clearSession();
      await navigateTo(
        createAccount ? Routes.CREATE_ACCOUNT : Routes.LOGIN_ACCOUNT
      );

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

      await loadSessionData();
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
    handleVerifyAccount,
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
