<template>
  <flex-box b="2">
    <trace-link-approval
      v-if="traceLink"
      :trace="traceLink"
      deletable
      @approve="handleClose"
      @decline="handleClose"
      @unreview="handleClose"
      @delete="handleClose"
    />
  </flex-box>
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
import { appStore, selectionStore } from "@/hooks";
import { FlexBox } from "@/components/common";
import { TraceLinkApproval } from "./index";

const traceLink = computed(() => selectionStore.selectedTraceLink);

/**
 * Closes this panel.
 */
function handleClose(): void {
  appStore.closeSidePanels();
}
</script>
