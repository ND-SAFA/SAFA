<template>
  <text-button
    v-if="appStore.runUpdate"
    text
    small
    color="accent"
    icon-id="mdi-cloud-sync-outline"
    data-cy="button-nav-load-update"
    @click="handleClick"
  >
    Load Project Updates
  </text-button>
</template>

<script lang="ts">
/**
 * Renders a button to update the current project.
 */
export default {
  name: "UpdateButton",
};
</script>

<script setup lang="ts">
import { appStore } from "@/hooks";
import { TextButton } from "@/components/common";

/**
 * Runs the current update.
 */
function handleClick(): void {
  appStore.loadAppChanges();
}
</script>
