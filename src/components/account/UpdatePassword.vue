<template>
  <v-card outlined class="pa-2 mb-2" style="width: 30em">
    <typography variant="subtitle" el="h2" value="Update Password" />
    <v-divider class="mb-2" />
    <typography
      el="p"
      value="Type in your current password and the new password you would like to set."
    />
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
    <v-card-actions>
      <v-btn
        :disabled="!oldPassword || !newPassword"
        outlined
        @click="handleEditPassword"
        data-cy="button-update-password"
      >
        Update Password
      </v-btn>
    </v-card-actions>
  </v-card>
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
     * Handles a password edit.
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
