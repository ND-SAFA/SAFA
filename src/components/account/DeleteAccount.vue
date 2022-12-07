<template>
  <panel-card style="width: 30em" color="error">
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
      label="Password"
      v-model="deletePassword"
      data-cy="input-delete-password"
    />
    <v-card-actions>
      <v-btn
        outlined
        color="error"
        :disabled="!deletePassword"
        @click="handleDeleteAccount"
        data-cy="button-delete-my-account"
      >
        Delete my account
      </v-btn>
    </v-card-actions>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { handleDeleteAccount } from "@/api";
import { PasswordField, Typography, PanelCard } from "@/components/common";

/**
 * Displays account deletion.
 */
export default Vue.extend({
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
