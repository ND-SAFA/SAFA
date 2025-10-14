<template>
  <private-page full-window>
    <settings-tabs />
  </private-page>
</template>

<script lang="ts">
/**
 * Displays project settings.
 */
export default {
  name: "ProjectSettingsView",
};
</script>

<script setup lang="ts">
import { PrivatePage, SettingsTabs } from "@/components";
</script>
