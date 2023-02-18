<template>
  <text-button
    v-if="runUpdate"
    text
    color="accent"
    variant="sync"
    data-cy="button-nav-load-update"
    @click="handleClick"
  >
    Load Changes
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
import { computed } from "vue";
import { appStore } from "@/hooks";
import { TextButton } from "@/components/common";

const runUpdate = computed(() => appStore.runUpdate);

/**
 * Runs the current update.
 */
function handleClick(): void {
  appStore.loadAppChanges();
}
</script>
