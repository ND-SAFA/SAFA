<template>
  <card-page id="login-view">
    <template #form>
      <email-input
        v-model="email"
        :error-message="errorMessage"
        @enter="handleSubmit"
      />
      <password-input v-model="password" @enter="handleSubmit" />
    </template>

    <template #actions>
      <text-button
        color="primary"
        label="Login"
        :disabled="password.length === 0"
        :loading="sessionApiStore.loading"
        class="login-button"
        data-cy="button-login"
        @click="handleSubmit"
      />

      <div class="q-ml-auto text-right">
        <div v-if="ENABLED_FEATURES.SIGN_UP">
          <typography value="Dont have an account yet?" />

          <text-button
            text
            small
            label="Sign Up"
            class="q-pl-sm"
            color="primary"
            data-cy="button-create-account-redirect"
            @click="handleSignUp"
          />
        </div>

        <text-button
          text
          small
          label="Forgot Password"
          color="primary"
          @click="handleForgotPassword"
        />
      </div>
    </template>
  </card-page>
</template>

<script lang="ts">
/**
 * Displays the login page.
 */
export default {
  name: "LoginView",
};
</script>

<script setup lang="ts">
import { ref, watch } from "vue";
import { ENABLED_FEATURES } from "@/util";
import { sessionApiStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  CardPage,
  PasswordInput,
  Typography,
  TextButton,
  EmailInput,
} from "@/components";

const email = ref("");
const password = ref("");
const errorMessage = ref<string | false>("");

/**
 * Navigate to the sign-up page.
 */
function handleSignUp() {
  navigateTo(Routes.CREATE_ACCOUNT);
}

/**
 * Navigate to the forgot password page.
 */
function handleForgotPassword() {
  navigateTo(Routes.FORGOT_PASSWORD);
}

/**
 * Attempts to log the user in.
 */
async function handleSubmit() {
  await sessionApiStore.handleLogin({
    email: email.value,
    password: password.value,
  });
}

watch(
  () => sessionApiStore.loginErrorMessage,
  (message) => (errorMessage.value = message)
);

watch(
  () => [email.value, password.value],
  () => (errorMessage.value = false)
);
</script>
