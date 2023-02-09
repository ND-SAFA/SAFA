<template>
  <panel-card>
    <typography variant="subtitle" el="h2" value="Theme" />
    <v-divider class="mb-2" />
    <switch-input
      label="Enable dark mode"
      :value="darkMode"
      @input="toggleTheme"
    />
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { useTheme } from "vuetify";
import { LocalStorageKeys } from "@/types";
import { PanelCard, Typography, SwitchInput } from "@/components/common";

/**
 * ThemeController
 */
export default Vue.extend({
  name: "ThemeController",
  components: { SwitchInput, PanelCard, Typography },
  setup() {
    const theme = useTheme();

    return {
      darkMode: theme.global.current.value.dark,
      toggleTheme: () => {
        const mode = theme.global.current.value.dark ? "light" : "dark";

        theme.global.name.value = mode;
        localStorage.setItem(LocalStorageKeys.darkMode, mode);
      },
    };
  },
});
</script>
