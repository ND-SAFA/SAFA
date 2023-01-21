<template>
  <div v-if="isOpen">
    <panel-card class="mt-2">
      <flex-box wrap>
        <attribute-chip artifact-type :value="sourceType" />
        <v-icon class="mx-1">mdi-ray-start-arrow</v-icon>
        <attribute-chip artifact-type :value="targetType" />
      </flex-box>
      <v-divider class="mt-1" />
      <typography variant="caption" value="Total Trace Links" />
      <typography el="p" :value="traceTotalCount" />
      <typography variant="caption" value="Generated Trace Links" />
      <typography el="p" :value="traceGeneratedCount" />
      <typography variant="caption" value="Approved Trace Links" />
      <typography el="p" :value="traceApprovedCount" />
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { TimTraceMatrixSchema } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  FlexBox,
} from "@/components/common";

/**
 * Displays trace matrix information.
 */
export default Vue.extend({
  name: "TraceMatrixPanel",
  components: { FlexBox, PanelCard, AttributeChip, Typography },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayTraceMatrix";
    },
    /**
     * @return The selected trace matrix
     */
    traceMatrix(): TimTraceMatrixSchema | undefined {
      return selectionStore.selectedTraceMatrix;
    },
    /**
     * @return The selected source artifact type.
     */
    sourceType(): string {
      return this.traceMatrix?.sourceType || "";
    },
    /**
     * @return The selected target artifact type.
     */
    targetType(): string {
      return this.traceMatrix?.targetType || "";
    },
    /**
     * @return The total number of traces between the selected types.
     */
    traceTotalCount(): string {
      const count = this.traceMatrix?.count || 0;

      return count === 1 ? "1 Link" : `${count} Links`;
    },
    /**
     * @return The number of generated traces between the selected types.
     */
    traceGeneratedCount(): string {
      const count = this.traceMatrix?.generatedCount || 0;

      return count === 1 ? "1 Link" : `${count} Links`;
    },
    /**
     * @return The number of approved traces between the selected types.
     */
    traceApprovedCount(): string {
      const count = this.traceMatrix?.approvedCount || 0;

      return count === 1 ? "1 Link" : `${count} Links`;
    },
  },
});
</script>
