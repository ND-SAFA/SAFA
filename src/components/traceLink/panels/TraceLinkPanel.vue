<template>
  <details-panel panel="displayTrace" data-cy="panel-trace-display">
    <trace-link-buttons />
    <trace-link-content />
  </details-panel>
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
import DetailsPanel from "@/components/navigation/detailsDrawer/DetailsPanel.vue";
import { TraceLinkButtons, TraceLinkContent } from "../display";
</script>
