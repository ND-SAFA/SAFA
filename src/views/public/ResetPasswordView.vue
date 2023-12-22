<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        value="Reset Password"
      />

      <div v-if="!sessionApiStore.passwordSubmitted">
        <typography b="2" el="p" value="Please enter a new password." />

        <password-input
          v-model="password"
          :error-message="sessionApiStore.passwordErrorMessage"
        />
      </div>

      <typography
        v-else
        el="p"
        value="Your password has been successfully updated."
      />
    </template>

    <template #actions>
      <text-button
        v-if="!sessionApiStore.passwordSubmitted"
        color="primary"
        label="Update Password"
        :disabled="password.length === 0"
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
 * Displays the reset password page.
 */
export default {
  name: "ResetPasswordView",
};
</script>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { sessionApiStore } from "@/hooks";
import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { CardPage, PasswordInput, Typography, TextButton } from "@/components";

const token = ref("");
const password = ref("");

/**
 * Navigates to the login page.
 */
function handleLogin() {
  navigateTo(Routes.LOGIN_ACCOUNT);
}

/**
 * Attempts to reset a user's password.
 */
function handleReset() {
  sessionApiStore.handlePasswordUpdate(password.value, token.value);
}

/**
 * Loads the password reset token on mount.
 */
onMounted(() => {
  const loadedToken = getParam(QueryParams.ACCOUNT_TOKEN);

  if (!loadedToken) return;

  token.value = String(loadedToken);
});
</script>
