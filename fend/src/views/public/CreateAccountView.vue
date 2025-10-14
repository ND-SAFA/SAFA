<template>
  <card-page>
    <template #form>
      <typography
        align="center"
        variant="title"
        el="h1"
        value="Welcome to SAFA!"
      />

      <div v-if="!sessionApiStore.createdAccount">
        <typography
          el="p"
          value="There are just a few key pieces of info we need to set up your account."
        />
        <email-input
          v-model="email"
          :error-message="sessionApiStore.createErrorMessage"
          data-cy="input-new-email"
        />
        <password-input v-model="password" data-cy="input-new-password" />
        <!--        <q-checkbox v-model="emailConsent" class="q-mb-md">-->
        <!--          <typography value="I agree to receive marketing emails." />-->
        <!--          <typography value=" Privacy Policy" />-->
        <!--        </q-checkbox>-->
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
        v-if="!sessionApiStore.createdAccount"
        color="primary"
        label="Create"
        :disabled="password.length === 0"
        data-cy="button-create-account"
        @click="handleCreateAccount"
      />

      <span class="q-ml-auto text-right">
        <typography value="Already have an account?" />

        <text-button
          text
          small
          label="Login"
          class="q-px-sm"
          color="primary"
          data-cy="button-create-account-login"
          @click="handleLogin"
        />
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
import { sessionApiStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  CardPage,
  PasswordInput,
  Typography,
  EmailInput,
  TextButton,
} from "@/components";

const email = ref("");
const password = ref("");
// const emailConsent = ref(false);

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
  sessionApiStore.handleCreateAccount({
    email: email.value,
    password: password.value,
  });
  email.value = "";
  password.value = "";
  // emailConsent.value = false;
}
</script>
