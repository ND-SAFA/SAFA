<template>
  <flex-box justify="center">
    <flex-item parts="12" class="q-mr-md">
      <log-out />
      <integrations-accounts />
      <api-keys-settings />
      <theme-controller />
      <update-password />
      <delete-account />
      <external-links />
    </flex-item>
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays information about the current user.
 */
export default {
  name: "MyAccount",
};
</script>

<script setup lang="ts">
import { FlexBox, FlexItem } from "@/components/common";
import { ExternalLinks } from "@/components/account/display";
import {
  ApiKeysSettings,
  IntegrationsAccounts,
  DeleteAccount,
  UpdatePassword,
  ThemeController,
  LogOut,
} from "@/components/account/save";
</script>
