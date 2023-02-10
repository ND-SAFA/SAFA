<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        class="mb-3"
        value="Forgot Password"
      />

      <div v-if="!isSubmitted">
        <typography
          el="p"
          b="2"
          value=" Please enter your email to reset your password."
        />

        <v-text-field
          v-model="email"
          filled
          label="Email"
          :error-messages="isError ? ['Unable to reset password'] : []"
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
        :disabled="email.length === 0"
        :loading="isLoading"
        @click="handleReset"
      >
        Reset Password
      </text-button>

      <span class="ml-auto">
        <text-button
          text
          small
          class="px-1"
          color="primary"
          @click="handleLogin"
        >
          Back To Login
        </text-button>
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
import TextButton from "@/components/common/button/TextButton.vue";
import { CardPage, Typography } from "@/components";

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
