<template>
  <card-page id="login-view">
    <template v-slot:form>
      <v-text-field
        filled
        label="Email"
        v-model="email"
        :error-messages="isError ? ['Invalid username or password'] : []"
        @keydown.enter="handleLogin"
      />
      <password-field v-model="password" @enter="handleLogin" />
    </template>

    <template v-slot:actions>
      <v-btn
        color="primary"
        width="8em"
        @click="handleLogin"
        :disabled="password.length === 0"
        :loading="isLoading"
      >
        Login
      </v-btn>

      <div class="ml-auto text-right">
        <span class="text-body-1">
          Dont have an account yet?

          <v-btn text small class="px-1" color="primary" @click="handleSignUp">
            Sign Up
          </v-btn>
        </span>

        <v-btn
          text
          small
          class="px-1"
          color="primary"
          @click="handleForgotPassword"
        >
          Forgot Password
        </v-btn>
      </div>
    </template>
  </card-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, Routes } from "@/router";
import { handleLogin } from "@/api";
import { CardPage, PasswordField } from "@/components";

/**
 * Displays the login page.
 */
export default Vue.extend({
  name: "LoginView",
  components: { PasswordField, CardPage },
  data() {
    return {
      email: "",
      password: "",
      isError: false,
      isLoading: false,
    };
  },
  methods: {
    /**
     * Navigate to the sign up page.
     */
    handleSignUp() {
      navigateTo(Routes.CREATE_ACCOUNT);
    },
    /**
     * Navigate to the forgot password page.
     */
    handleForgotPassword() {
      navigateTo(Routes.FORGOT_PASSWORD);
    },
    /**
     * Attempts to log the user in.
     */
    handleLogin() {
      this.isLoading = true;

      handleLogin({
        email: this.email,
        password: this.password,
      })
        .then(() => (this.isError = false))
        .catch(() => (this.isError = true))
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
