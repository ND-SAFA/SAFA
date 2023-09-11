<template>
  <flex-box>
    <flex-item parts="6" class="q-mr-md">
      <theme-controller />
      <update-password />
      <delete-account />
    </flex-item>
    <flex-item parts="6">
      <external-links />
      <integrations-accounts />
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
  IntegrationsAccounts,
  DeleteAccount,
  UpdatePassword,
  ThemeController,
} from "@/components/account/save";
</script>
