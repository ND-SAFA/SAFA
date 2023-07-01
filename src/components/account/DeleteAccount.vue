<template>
  <panel-card color="negative" title="Delete Account">
    <typography
      el="p"
      value="Type in your current password to delete your account."
    />
    <password-input
      v-model="password"
      label="Password"
      data-cy="input-delete-password"
    />
    <template #actions>
      <text-button
        label="Delete My Account"
        outlined
        color="negative"
        :disabled="!password"
        data-cy="button-delete-my-account"
        @click="handleSubmit"
      />
    </template>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays account deletion.
 */
export default {
  name: "DeleteAccount",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { sessionApiStore } from "@/hooks";
import {
  PasswordInput,
  Typography,
  PanelCard,
  TextButton,
} from "@/components/common";

const password = ref("");

/**
 * Handles account deletion.
 */
function handleSubmit(): void {
  sessionApiStore.handleDeleteAccount(password.value);
}
</script>
