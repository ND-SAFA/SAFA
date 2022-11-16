<template>
  <private-page full-window>
    <template v-slot:page>
      <settings-tabs />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, SettingsTabs } from "@/components";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "ProjectSettingsView",
  components: {
    PrivatePage,
    SettingsTabs,
  },
});
</script>
