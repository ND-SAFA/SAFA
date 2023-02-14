<template>
  <panel-card>
    <typography variant="subtitle" el="h2" value="Update Password" />
    <v-divider class="mb-2" />
    <typography
      el="p"
      value="Type in your current password and the new password you would like to set."
    />
    <password-field
      v-model="oldPassword"
      label="Current Password"
      :errors="passwordErrors"
      data-cy="input-current-password"
    />
    <password-field
      v-model="newPassword"
      label="New Password"
      data-cy="input-new-password"
    />
    <v-card-actions>
      <v-btn
        :disabled="!oldPassword || !newPassword"
        outlined
        data-cy="button-update-password"
        @click="handleEditPassword"
      >
        Update Password
      </v-btn>
    </v-card-actions>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { handleChangePassword } from "@/api";
import { PasswordField, Typography, PanelCard } from "@/components/common";

/**
 * Allows for password updating.
 */
export default defineComponent({
  name: "MyAccountView",
  components: {
    PanelCard,
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
