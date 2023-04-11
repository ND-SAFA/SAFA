<template>
  <card-page id="login-view">
    <template #form>
      <text-input
        v-model="email"
        label="Email"
        :error-message="isError && 'Invalid username or password'"
        data-cy="input-email"
        @enter="handleSubmit"
      />
      <password-input v-model="password" @enter="handleSubmit" />
    </template>

    <template #actions>
      <text-button
        color="primary"
        label="Login"
        :disabled="password.length === 0"
        :loading="isLoading"
        class="login-button"
        data-cy="button-login"
        @click="handleSubmit"
      />

      <div class="q-ml-auto text-right">
        <div>
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
import { ref } from "vue";
import { navigateTo, Routes } from "@/router";
import { handleLogin } from "@/api";
import {
  CardPage,
  PasswordInput,
  Typography,
  TextButton,
  TextInput,
} from "@/components";

const email = ref("");
const password = ref("");
const isError = ref(false);
const isLoading = ref(false);

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
function handleSubmit() {
  isLoading.value = true;

  handleLogin({
    email: email.value,
    password: password.value,
  })
    .then(() => (isError.value = false))
    .catch(() => (isError.value = true))
    .finally(() => (isLoading.value = false));
}
</script>
