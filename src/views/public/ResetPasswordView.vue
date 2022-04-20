<template>
  <card-page>
    <template v-slot:form>
      <h2 class="text-h4 mb-3 text-center">Reset Password</h2>

      <div v-if="!isSubmitted">
        <p class="text-body-1">Please enter a new password.</p>

        <password-field v-model="password" />
      </div>

      <p v-else class="text-body-1">
        Your password has been successfully updated.
      </p>
    </template>

    <template v-slot:actions>
      <v-btn
        v-if="!isSubmitted"
        color="primary"
        @click="handleReset"
        :disabled="password.length === 0"
        :loading="isLoading"
      >
        Update Password
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
import { updatePassword } from "@/api";
import { CardPage, PasswordField } from "@/components";

/**
 * Displays the reset password page.
 */
export default Vue.extend({
  name: "ResetPasswordView",
  components: { PasswordField, CardPage },
  data() {
    return {
      password: "",
      token: "",
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
     * Attempts to reset a user's password.
     */
    handleReset() {
      this.isLoading = true;

      updatePassword({
        password: this.password,
        token: this.token,
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
