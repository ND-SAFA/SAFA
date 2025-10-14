<template>
  <details-panel panel="displayTrace" data-cy="panel-trace-display">
    <template #actions>
      <trace-link-buttons />
    </template>
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
import { DetailsPanel } from "@/components/common";
import { TraceLinkContent } from "@/components/traceLink/display";
import { TraceLinkButtons } from "@/components/traceLink/save";
</script>
