<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        value="Forgot Password"
      />

      <div v-if="!isSubmitted">
        <typography
          el="p"
          b="2"
          value=" Please enter your email to reset your password."
        />

        <text-input
          v-model="email"
          label="Email"
          :error-message="isError && 'Unable to reset password'"
        />
      </div>

      <typography
        v-else
        el="p"
        value="If you have an existing account, your password has successfully been
        reset. Please check your email to complete the password reset process."
      />
    </template>

    <template #actions>
      <text-button
        v-if="!isSubmitted"
        color="primary"
        label="Reset Password"
        :disabled="email.length === 0"
        :loading="isLoading"
        @click="handleReset"
      />

      <span class="q-ml-auto">
        <text-button
          text
          small
          label="Back To Login"
          color="primary"
          @click="handleLogin"
        />
      </span>
    </template>
  </card-page>
</template>

<script lang="ts">
/**
 * Displays the forgot password page.
 */
export default {
  name: "ForgotPasswordView",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { navigateTo, Routes } from "@/router";
import { createPasswordReset } from "@/api";
import { CardPage, Typography, TextButton, TextInput } from "@/components";

const email = ref("");
const isError = ref(false);
const isLoading = ref(false);
const isSubmitted = ref(false);

/**
 * Navigates to the login page.
 */
function handleLogin() {
  navigateTo(Routes.LOGIN_ACCOUNT);
}

/**
 * Sends a password reset email.
 */
function handleReset() {
  isLoading.value = true;

  createPasswordReset({
    email: email.value,
  })
    .then(() => {
      isSubmitted.value = true;
      isError.value = false;
    })
    .catch(() => (isError.value = true))
    .finally(() => (isLoading.value = false));
}
</script>
