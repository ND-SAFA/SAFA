<template>
  <div v-if="isOpen">
    <panel-card class="mt-2">
      <flex-box wrap>
        <attribute-chip artifact-type :value="sourceType" />
        <v-icon class="mx-1">mdi-ray-start-arrow</v-icon>
        <attribute-chip artifact-type :value="targetType" />
      </flex-box>
      <v-divider class="mt-1" />
      <typography variant="caption" value="Details" />
      <typography el="p" :value="traceCount" />
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
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
     * @return The selected source artifact type.
     */
    sourceType(): string {
      return selectionStore.selectedTraceMatrix?.sourceType || "";
    },
    /**
     * @return The selected target artifact type.
     */
    targetType(): string {
      return selectionStore.selectedTraceMatrix?.targetType || "";
    },
    /**
     * @return The number of traces between the selected types.
     */
    traceCount(): string {
      const count = selectionStore.selectedTraceMatrix?.count || 0;

      return count === 1 ? "1 Trace Links" : `${count} Trace Links`;
    },
  },
});
</script>
