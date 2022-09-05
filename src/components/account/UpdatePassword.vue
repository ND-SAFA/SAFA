<template>
  <div style="max-width: 300px">
    <typography variant="subtitle" el="h2" value="Password" y="2" />
    <password-field
      label="Current Password"
      v-model="oldPassword"
      :errors="passwordErrors"
      data-cy="input-current-password"
    />
    <password-field
      label="New Password"
      v-model="newPassword"
      data-cy="input-new-password"
    />
    <v-btn
      :disabled="!oldPassword || !newPassword"
      outlined
      @click="handleEditPassword"
      data-cy="button-update-password"
    >
      Update Password
    </v-btn>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { handleChangePassword } from "@/api";
import { PasswordField, Typography } from "@/components";

/**
 * Allows for password updating.
 */
export default Vue.extend({
  name: "MyAccountView",
  components: {
    Typography,
    PasswordField,
  },
  data() {
    return {
      oldPassword: "",
      newPassword: "",
      passwordError: false,
    };
  },
  computed: {
    /**
     * @return The current password errors.
     */
    passwordErrors(): string[] {
      return this.passwordError ? ["Incorrect password"] : [];
    },
  },
  methods: {
    /**
     * Handles an password edit.
     */
    handleEditPassword(): void {
      this.passwordError = false;

      handleChangePassword(
        {
          oldPassword: this.oldPassword,
          newPassword: this.newPassword,
        },
        {
          onSuccess: () => {
            this.oldPassword = "";
            this.newPassword = "";
          },
          onError: () => (this.passwordError = true),
        }
      );
    },
  },
});
</script>
