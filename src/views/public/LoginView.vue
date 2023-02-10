<template>
  <card-page id="login-view">
    <template #form>
      <v-text-field
        v-model="email"
        filled
        label="Email"
        :error-messages="isError ? ['Invalid username or password'] : []"
        data-cy="input-email"
        @keydown.enter="handleLogin"
      />
      <password-field v-model="password" @enter="handleLogin" />
    </template>

    <template #actions>
      <text-button
        color="primary"
        width="8em"
        :disabled="password.length === 0"
        :loading="isLoading"
        data-cy="button-login"
        @click="handleSubmit"
      >
        Login
      </text-button>

      <div class="ml-auto text-right">
        <span>
          <typography value="Dont have an account yet?" />

          <text-button
            text
            small
            class="px-1"
            color="primary"
            data-cy="button-create-account-redirect"
            @click="handleSignUp"
          >
            Sign Up
          </text-button>
        </span>

        <text-button
          text
          small
          class="px-1"
          color="primary"
          @click="handleForgotPassword"
        >
          Forgot Password
        </text-button>
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
import { useRouter } from "vue-router";
import { Routes } from "@/router";
import { handleLogin } from "@/api";
import TextButton from "@/components/common/button/TextButton.vue";
import { CardPage, PasswordField, Typography } from "@/components";

const router = useRouter();
const email = ref("");
const password = ref("");
const isError = ref(false);
const isLoading = ref(false);

/**
 * Navigate to the sign-up page.
 */
function handleSignUp() {
  router.push(Routes.CREATE_ACCOUNT);
}

/**
 * Navigate to the forgot password page.
 */
function handleForgotPassword() {
  router.push(Routes.FORGOT_PASSWORD);
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
