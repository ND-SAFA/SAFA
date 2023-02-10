<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        class="mb-3"
        value="Welcome to SAFA!"
      />

      <div v-if="!isCreated">
        <typography
          el="p"
          value="There are just a few key pieces of info we need to set up your account."
        />

        <v-text-field
          v-model="email"
          filled
          label="Email"
          :error-messages="isError ? ['Unable to create an account'] : []"
          data-cy="input-new-email"
        />
        <password-field v-model="password" data-cy="input-new-password" />
      </div>

      <typography
        v-else
        el="p"
        value="Your account has been successfully created. Please check your email to
        complete the sign up process."
      />
    </template>

    <template #actions>
      <text-button
        v-if="!isCreated"
        color="primary"
        :disabled="password.length === 0"
        data-cy="button-create-account"
        @click="handleCreateAccount"
      >
        Create Account
      </text-button>

      <span class="ml-auto text-right text-body-1">
        <typography value="Already have an account?" />

        <text-button
          text
          small
          class="px-1"
          color="primary"
          data-cy="button-create-account-login"
          @click="handleLogin"
        >
          Login
        </text-button>
      </span>
    </template>
  </card-page>
</template>

<script lang="ts">
/**
 * Displays the create account page.
 */
export default {
  name: "CreateAccountView",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { navigateTo, Routes } from "@/router";
import { createUser } from "@/api";
import TextButton from "@/components/common/button/TextButton.vue";
import { CardPage, PasswordField, Typography } from "@/components";

const email = ref("");
const password = ref("");
const isError = ref(false);
const isLoading = ref(false);
const isCreated = ref(false);

/**
 * Navigates to the login page.
 */
function handleLogin() {
  navigateTo(Routes.LOGIN_ACCOUNT);
}

/**
 * Attempts to create a new account.
 */
function handleCreateAccount() {
  isLoading.value = true;

  createUser({
    email: email.value,
    password: password.value,
  })
    .then(() => {
      isError.value = false;
      isCreated.value = true;
    })
    .catch(() => (isError.value = true))
    .finally(() => (isLoading.value = false));
}
</script>
