<template>
  <card-page>
    <template v-slot:form>
      <v-text-field
        filled
        label="Email"
        v-model="email"
        :error-messages="isError ? ['Invalid username or password'] : []"
        @keydown.enter="handleLogin"
      />
      <password-field v-model="password" @submit="handleLogin" />
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
import { CardPage, PasswordField } from "@/components";
import { navigateTo, Routes } from "@/router";
import { loadLastProject } from "@/api";
import { login } from "@/api/handlers/session-handler";

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
    isLoading: false,
  }),
  methods: {
    handleLogin() {
      const goToPage = new URLSearchParams(window.location.search).get("to");

      this.isLoading = true;

      login({
        email: this.email,
        password: this.password,
      })
        .then(async () => {
          this.isLoading = false;

          if (goToPage && goToPage !== Routes.ARTIFACT_TREE) {
            await navigateTo(goToPage);
          } else {
            await loadLastProject();
          }
        })
        .catch(() => {
          this.isError = true;
          this.isLoading = false;
        });
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
