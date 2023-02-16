<template>
  <panel-card>
    <typography variant="subtitle" el="h2" value="Theme" />
    <v-divider class="mb-2" />
    <switch-input
      label="Enable dark mode"
      :model-value="darkMode"
      @input="toggleDarkMode"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Injects the app theme.
 */
export default {
  name: "ThemeController",
};
</script>

<script setup lang="ts">
import { useTheme } from "@/hooks";
import { PanelCard, Typography, SwitchInput } from "@/components/common";

const { darkMode, toggleDarkMode } = useTheme();
</script>
