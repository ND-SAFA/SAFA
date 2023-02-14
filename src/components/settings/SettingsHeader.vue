<template>
  <div>
    <back-button text="Back To Tree View" to-project />
    <typography t="2" el="h1" variant="title" value="Project Settings" />
    <v-divider class="mb-2" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Typography, BackButton } from "@/components/common";

/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default defineComponent({
  name: "SettingsHeader",
  components: {
    Typography,
    BackButton,
  },
});
</script>
