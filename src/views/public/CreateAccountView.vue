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
        @click="handleCreateAccount"
        :disabled="password.length === 0"
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
import { CardPage, PasswordField } from "@/components";
import { navigateTo, Routes } from "@/router";
import { createUser } from "@/api";

/**
 * Presents the create account page.
 */
export default Vue.extend({
  name: "create-account-view",
  components: { CardPage, PasswordField },
  data: () => ({
    email: "",
    password: "",
    isError: false,
    isCreated: false,
  }),
  methods: {
    handleLogin() {
      navigateTo(Routes.LOGIN_ACCOUNT);
    },
    handleCreateAccount() {
      createUser({
        email: this.email,
        password: this.password,
      })
        .then(() => {
          this.isCreated = true;
          this.isError = false;
        })
        .catch(() => (this.isError = true));
    },
  },
});
</script>
