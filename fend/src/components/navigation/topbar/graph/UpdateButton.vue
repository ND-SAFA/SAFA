<template>
  <text-button
    v-if="appStore.runUpdate"
    text
    label="Load Changes"
    color="primary"
    icon="sync"
    data-cy="button-nav-load-update"
    @click="appStore.loadAppChanges()"
  />
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
</script>
