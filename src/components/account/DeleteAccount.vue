<template>
  <div style="max-width: 300px">
    <typography variant="subtitle" el="h2" value="Danger Zone" y="2" />
    <password-field label="Password" v-model="deletePassword" />
    <v-btn
      outlined
      color="error"
      :disabled="!deletePassword"
      @click="handleDeleteAccount"
    >
      Delete my account
    </v-btn>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PasswordField, Typography } from "@/components";
import { handleDeleteAccount } from "@/api";

/**
 * Displays account deletion.
 */
export default Vue.extend({
  name: "DeleteAccount",
  components: {
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
