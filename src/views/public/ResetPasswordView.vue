<template>
  <card-page>
    <template v-slot:form>
      <typography
        align="center"
        variant="title"
        el="h1"
        class="mb-3"
        value="Reset Password"
      />

      <div v-if="!isSubmitted">
        <typography el="p" value="Please enter a new password." />

        <password-field v-model="password" />
      </div>

      <typography
        v-else
        el="p"
        value="Your password has been successfully updated."
      />
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
import { CardPage, PasswordField, Typography } from "@/components";

/**
 * Displays the reset password page.
 */
export default Vue.extend({
  name: "ResetPasswordView",
  components: { PasswordField, CardPage, Typography },
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
