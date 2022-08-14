<template>
  <card-page>
    <template v-slot:form>
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
          outlined
          label="Email"
          v-model="email"
          :error-messages="isError ? ['Unable to create an account'] : []"
          data-cy="input-email"
        />
        <password-field v-model="password" />
      </div>

      <typography
        v-else
        el="p"
        value="Your account has been successfully created. Please check your email to
        complete the sign up process."
      />
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
        <typography value="Already have an account?" />

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
import { CardPage, PasswordField, Typography } from "@/components";

/**
 * Displays the create account page.
 */
export default Vue.extend({
  name: "CreateAccountView",
  components: { CardPage, PasswordField, Typography },
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
