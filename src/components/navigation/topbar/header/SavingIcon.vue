<template>
  <v-tooltip v-if="appStore.isSaving" bottom z-index="10000">
    <template #activator="{ on, attrs }">
      <v-progress-circular
        v-bind="attrs"
        indeterminate
        size="36"
        color="accent"
        v-on="on"
      >
        <v-icon color="accent"> mdi-cloud-upload-outline </v-icon>
      </v-progress-circular>
    </template>
    <span>Saving...</span>
  </v-tooltip>
</template>

<script lang="ts">
/**
 * Renders app saving state.
 */
export default {
  name: "SavingIcon",
};
</script>

<script setup lang="ts">
import { appStore } from "@/hooks";
</script>
