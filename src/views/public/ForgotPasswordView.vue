<template>
  <card-page>
    <template v-slot:form>
      <typography
        align="center"
        variant="title"
        el="h1"
        class="mb-3"
        value="Forgot Password"
      />

      <div v-if="!isSubmitted">
        <typography
          el="p"
          value=" Please enter your email to reset your password."
        />

        <v-text-field
          filled
          label="Email"
          v-model="email"
          :error-messages="isError ? ['Unable to reset password'] : []"
        />
      </div>

      <typography
        v-else
        el="p"
        value="If you have an existing account, your password has successfully been
        reset. Please check your email to complete the password reset process."
      />
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
import { CardPage, Typography } from "@/components";

/**
 * Displays the forgot password page.
 */
export default Vue.extend({
  name: "ForgotPasswordView",
  components: { CardPage, Typography },
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
        userId: "822d5f34-5154-11ed-bdc3-0242ac120002",
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
