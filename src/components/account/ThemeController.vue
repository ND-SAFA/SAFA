<template>
  <panel-card>
    <typography variant="subtitle" el="h2" value="Theme" />
    <v-divider class="mb-2" />
    <switch-input v-model="darkMode" label="Enable dark mode" />
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { LocalStorageKeys } from "@/types";
import { PanelCard, Typography, SwitchInput } from "@/components/common";

/**
 * ThemeController
 */
export default Vue.extend({
  name: "ThemeController",
  components: { SwitchInput, PanelCard, Typography },
  computed: {
    darkMode: {
      get(): boolean {
        return this.$vuetify.theme.dark;
      },
      set(dark: boolean): void {
        this.$vuetify.theme.dark = dark;
        localStorage.setItem(LocalStorageKeys.darkMode, String(dark));
      },
    },
  },
});
</script>
