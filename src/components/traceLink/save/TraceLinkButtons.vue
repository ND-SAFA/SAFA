<template>
  <trace-link-approval
    v-if="traceLink"
    :trace="traceLink"
    deletable
    @approve="handleClose"
    @decline="handleClose"
    @unreview="handleClose"
    @delete="handleClose"
  />
</template>

<script lang="ts">
/**
 * Displays buttons for the selected trace link.
 */
export default {
  name: "TraceLinkButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, traceStore } from "@/hooks";
import TraceLinkApproval from "./TraceLinkApproval.vue";

const traceLink = computed(() => traceStore.selectedTraceLink);

/**
 * Closes this panel.
 */
function handleClose(): void {
  appStore.closeSidePanels();
}
</script>
