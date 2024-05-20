<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        value="Forgot Password"
      />

      <div v-if="!sessionApiStore.passwordSubmitted">
        <typography
          el="p"
          b="2"
          value=" Please enter your email to reset your password."
        />

        <email-input
          v-model="email"
          :error-message="sessionApiStore.passwordErrorMessage"
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
        v-if="!sessionApiStore.passwordSubmitted"
        color="primary"
        label="Reset Password"
        :disabled="email.length === 0"
        :loading="sessionApiStore.loading"
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
import { sessionApiStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { CardPage, Typography, TextButton, EmailInput } from "@/components";

const email = ref("");

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
  sessionApiStore.handlePasswordReset(email.value);
}
</script>
