<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        class="mb-3"
        value="Reset Password"
      />

      <div v-if="!isSubmitted">
        <typography b="2" el="p" value="Please enter a new password." />

        <password-field v-model="password" :errors="errors" />
      </div>

      <typography
        v-else
        el="p"
        value="Your password has been successfully updated."
      />
    </template>

    <template #actions>
      <text-button
        v-if="!isSubmitted"
        color="primary"
        :disabled="password.length === 0"
        :loading="isLoading"
        @click="handleReset"
      >
        Update Password
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
 * Displays the reset password page.
 */
export default {
  name: "ResetPasswordView",
};
</script>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getParam, navigateTo, QueryParams, Routes } from "@/router";
import { updatePassword } from "@/api";
import TextButton from "@/components/common/button/TextButton.vue";
import { CardPage, PasswordField, Typography } from "@/components";

const token = ref("");
const password = ref("");
const isError = ref(false);
const isLoading = ref(false);
const isSubmitted = ref(false);

const errors = computed(() =>
  isError.value ? ["Unable to reset your password."] : []
);

onMounted(() => {
  const loadedToken = getParam(QueryParams.PW_RESET);

  if (!loadedToken) return;

  token.value = String(loadedToken);
});

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
  isLoading.value = true;

  updatePassword({
    newPassword: password.value,
    resetToken: token.value,
  })
    .then(() => {
      isSubmitted.value = true;
      isError.value = false;
    })
    .catch(() => (isError.value = true))
    .finally(() => (isLoading.value = false));
}
</script>
