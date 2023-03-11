<template>
  <panel-card title="Update Password">
    <typography
      el="p"
      value="Type in your current password and the new password you would like to set."
    />
    <password-input
      v-model="oldPassword"
      label="Current Password"
      :errors="errorText"
      data-cy="input-current-password"
    />
    <password-input
      v-model="newPassword"
      label="New Password"
      data-cy="input-new-password"
    />
    <template #actions>
      <text-button
        label="Update Password"
        :disabled="isDisabled"
        outlined
        data-cy="button-update-password"
        @click="handleEditPassword"
      />
    </template>
  </panel-card>
</template>

<script lang="ts">
/**
 * Allows for password updating.
 */
export default {
  name: "MyAccountView",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { handleChangePassword } from "@/api";
import {
  PasswordInput,
  Typography,
  PanelCard,
  TextButton,
} from "@/components/common";

const oldPassword = ref("");
const newPassword = ref("");
const error = ref(false);

const errorText = computed(() => error.value && "Incorrect password");
const isDisabled = computed(() => !oldPassword.value || !newPassword.value);

/**
 * Handles a password edit.
 */
function handleEditPassword(): void {
  error.value = false;

  handleChangePassword(
    {
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    },
    {
      onSuccess: () => {
        oldPassword.value = "";
        newPassword.value = "";
      },
      onError: () => (error.value = true),
    }
  );
}
</script>
