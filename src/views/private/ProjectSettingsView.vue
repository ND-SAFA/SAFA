<template>
  <private-page>
    <template v-slot:page>
      <back-button text="Back To Tree View" to-project />
      <settings-tabs />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, SettingsTabs, BackButton } from "@/components";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "ProjectSettingsView",
  components: {
    BackButton,
    PrivatePage,
    SettingsTabs,
  },
  computed: {},
});
</script>
