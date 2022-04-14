<template>
  <card-page>
    <template v-slot:form>
      <h2 class="text-h4 mb-3 text-center">Forgot Password</h2>

      <div v-if="!isSubmitted">
        <p class="text-body-1">
          Please enter your email to reset your password.
        </p>

        <v-text-field
          filled
          label="Email"
          v-model="email"
          :error-messages="isError ? ['Unable to reset password'] : []"
        />
      </div>

      <p v-else class="text-body-1">
        If you have an existing account, your password has successfully been
        reset. Please check your email to complete the password reset process.
      </p>
    </template>

    <template v-slot:actions>
      <v-btn
        v-if="!isSubmitted"
        color="primary"
        @click="handleReset"
        :disabled="email.length === 0"
        :loading="isLoading"
      >
        Reset Password
      </v-btn>

      <span class="ml-auto">
        <v-btn text small class="px-1" color="primary" @click="handleLogin">
          Back To Login
        </v-btn>
      </span>
    </template>
  </card-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, Routes } from "@/router";
import { createPasswordReset } from "@/api";
import { CardPage } from "@/components";

/**
 * Displays the forgot password page.
 */
export default Vue.extend({
  name: "ForgotPasswordView",
  components: { CardPage },
  data() {
    return {
      email: "",
      isSubmitted: false,
      isError: false,
      isLoading: false,
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
     * Sends a password reset email.
     */
    handleReset() {
      this.isLoading = true;

      createPasswordReset({
        email: this.email,
      })
        .then(() => {
          this.isSubmitted = true;
          this.isError = false;
        })
        .catch(() => (this.isError = true))
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
