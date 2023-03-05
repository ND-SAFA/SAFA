<template>
  <flex-box y="4">
    <trace-link-approval
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
import { defineComponent } from "vue";
import { TraceLinkSchema } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { FlexBox } from "@/components/common";
import { TraceLinkApproval } from "./index";

/**
 * Displays buttons for the selected trace link.
 */
export default defineComponent({
  name: "TraceLinkButtons",
  components: { TraceLinkApproval, FlexBox },
  computed: {
    /**
     * @return The selected trace link.
     */
    traceLink(): TraceLinkSchema | undefined {
      return selectionStore.selectedTraceLink;
    },
  },
  methods: {
    /**
     * Closes this panel.
     */
    handleClose(): void {
      appStore.closeSidePanels();
    },
  },
});
</script>

<style scoped lang="scss"></style>
