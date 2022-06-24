<template>
  <card-page>
    <template v-slot:form>
      <h2 class="text-h4 mb-3 text-center">Welcome to SAFA!</h2>

      <div v-if="!isCreated">
        <p class="text-body-1">
          There are just a few key pieces of info we need to set up your
          account.
        </p>

        <v-text-field
          filled
          label="Email"
          v-model="email"
          :error-messages="isError ? ['Unable to create an account'] : []"
          data-cy="input-email"
        />
        <password-field v-model="password" />
      </div>

      <p v-else class="text-body-1">
        Your account has been successfully created. Please check your email to
        complete the sign up process.
      </p>
    </template>

    <template v-slot:actions>
      <v-btn
        v-if="!isCreated"
        color="primary"
        :disabled="password.length === 0"
        data-cy="button-create-account"
        @click="handleCreateAccount"
      >
        Create Account
      </v-btn>

      <span class="ml-auto text-right text-body-1">
        Already have an account?

        <v-btn text small class="px-1" color="primary" @click="handleLogin">
          Login
        </v-btn>
      </span>
    </template>
  </card-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, Routes } from "@/router";
import { createUser } from "@/api";
import { CardPage, PasswordField } from "@/components";

/**
 * Displays the create account page.
 */
export default Vue.extend({
  name: "CreateAccountView",
  components: { CardPage, PasswordField },
  data() {
    return {
      email: "",
      password: "",
      isError: false,
      isLoading: false,
      isCreated: false,
    };
  },
  methods: {
    /**
     * Navigates to the login page.
     */
    handleLogin() {
      navigateTo(Routes.LOGIN_ACCOUNT);
    },
    /**
     * Attempts to create a new account.
     */
    handleCreateAccount() {
      this.isLoading = true;

      createUser({
        email: this.email,
        password: this.password,
      })
        .then(() => {
          this.isError = false;
          this.isCreated = true;
        })
        .catch(() => (this.isError = true))
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
