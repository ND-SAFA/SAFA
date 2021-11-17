<template>
  <card-page>
    <template v-slot:form>
      <v-text-field
        filled
        label="Email"
        v-model="email"
        :error-messages="isError ? ['Invalid username or password'] : []"
      />
      <password-field v-model="password" />
    </template>

    <template v-slot:actions>
      <v-btn
        color="primary"
        width="8em"
        @click="handleLogin"
        :disabled="password.length === 0"
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
import { CardPage, PasswordField } from "@/components";
import router, { navigateTo, Routes } from "@/router";
import { sessionModule } from "@/store";

/**
 * Presents the login page.
 */
export default Vue.extend({
  name: "login-view",
  components: { PasswordField, CardPage },
  data: () => ({
    email: "",
    password: "",
    isError: false,
  }),
  methods: {
    handleLogin() {
      const goToPage =
        new URLSearchParams(window.location.search).get("to") || Routes.HOME;

      sessionModule
        .login({
          email: this.email,
          password: this.password,
        })
        .then(() => navigateTo(goToPage))
        .catch(() => (this.isError = true));
    },
    handleSignUp() {
      navigateTo(Routes.CREATE_ACCOUNT);
    },
    handleForgotPassword() {
      navigateTo(Routes.FORGOT_PASSWORD);
    },
  },
});
</script>
