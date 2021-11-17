<template>
  <card-page>
    <template v-slot:form>
      <v-text-field filled label="Email" v-model="email" />
      <v-text-field
        filled
        label="Password"
        v-model="password"
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        @click:append="showPassword = !showPassword"
      />
    </template>

    <template v-slot:actions>
      <v-btn color="primary" width="8em">Login</v-btn>

      <div class="text-body-1 ml-auto text-right">
        <p class="mb-0">
          Dont have an account yet?
          <v-btn text small class="px-1" color="primary">Sign Up</v-btn>
        </p>
        <v-btn text small class="px-1" color="primary">Forgot Password</v-btn>
      </div>
    </template>
  </card-page>
</template>

<script lang="ts">
import Vue from "vue";
import { CardPage } from "@/components";

/**
 * Presents the login page.
 */
export default Vue.extend({
  name: "login-view",
  components: { CardPage },
  data: () => ({
    email: "",
    password: "",
    showPassword: false,
  }),
  methods: {
    onLogin() {
      console.log(this.email, this.password);
    },
    onSignUp() {
      console.log(this.email, this.password);
    },
    onForgotPassword() {
      console.log(this.email, this.password);
    },
  },
});
</script>
