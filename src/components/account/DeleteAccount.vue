<template>
  <panel-card color="error">
    <typography
      variant="subtitle"
      el="h2"
      value="Delete Account"
      color="error"
    />
    <v-divider class="mb-2" />
    <typography
      el="p"
      value="Type in your current password to delete your account."
    />
    <password-field
      v-model="deletePassword"
      label="Password"
      data-cy="input-delete-password"
    />
    <v-card-actions>
      <v-btn
        outlined
        color="error"
        :disabled="!deletePassword"
        data-cy="button-delete-my-account"
        @click="handleDeleteAccount"
      >
        Delete my account
      </v-btn>
    </v-card-actions>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { handleDeleteAccount } from "@/api";
import { PasswordField, Typography, PanelCard } from "@/components/common";

/**
 * Displays account deletion.
 */
export default defineComponent({
  name: "DeleteAccount",
  components: {
    PanelCard,
    Typography,
    PasswordField,
  },
  data() {
    return {
      deletePassword: "",
      passwordError: false,
    };
  },
  methods: {
    /**
     * Handles account deletion.
     */
    handleDeleteAccount(): void {
      handleDeleteAccount(this.deletePassword);
    },
  },
});
</script>
