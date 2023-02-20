<template>
  <panel-card title="Theme">
    <switch-input
      label="Enable dark mode"
      :model-value="darkMode"
      @update:model-value="toggleDarkMode"
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
import { PanelCard, SwitchInput } from "@/components/common";

const { darkMode, toggleDarkMode } = useTheme();
</script>
