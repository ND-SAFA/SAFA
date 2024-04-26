<template>
  <details-panel panel="generateTrace" data-cy="panel-trace-display">
    <panel-card title="Generate Trace Links" borderless>
      <trace-link-generator :open="isOpen" @submit="handleClose" />
    </panel-card>
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
import { computed } from "vue";
import { appStore } from "@/hooks";
import { DetailsPanel, PanelCard } from "@/components/common";
import { TraceLinkGenerator } from "@/components/traceLink/save";

const isOpen = computed(() => appStore.popups.detailsPanel === "generateTrace");

/**
 * Closes all side panels.
 */
function handleClose(): void {
  appStore.closeSidePanels();
}
</script>
