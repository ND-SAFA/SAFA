<template>
  <div v-if="isOpen" data-cy="panel-trace-display">
    <trace-link-buttons />
    <trace-link-content />
  </div>
</template>

<script lang="ts">
/**
 * Displays trace link information.
 */
export default {
  name: "TraceLinkPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore } from "@/hooks";
import { TraceLinkButtons, TraceLinkContent } from "../display";

const isOpen = computed(() => appStore.isDetailsPanelOpen === "displayTrace");
</script>
