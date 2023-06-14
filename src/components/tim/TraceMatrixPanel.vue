<template>
  <details-panel panel="displayTraceMatrix">
    <flex-box b="2">
      <text-button
        text
        label="View In Tree"
        icon="artifact"
        @click="handleViewLevel"
      />
    </flex-box>

    <panel-card :title="`${sourceType} to ${targetType}`">
      <template #title-actions>
        <icon
          class="q-mx-xs"
          size="sm"
          color="primary"
          variant="trace"
          :rotate="-90"
        />
      </template>
      <typography variant="caption" value="Total Trace Links" />
      <typography el="p" :value="totalCount" />
      <typography variant="caption" value="Generated Trace Links" />
      <typography el="p" :value="generatedCount" />
      <typography variant="caption" value="Approved Trace Links" />
      <typography el="p" :value="approvedCount" />
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays trace matrix information.
 */
export default {
  name: "TraceMatrixPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { documentStore, selectionStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  FlexBox,
  TextButton,
  Icon,
  DetailsPanel,
} from "@/components/common";

const traceMatrix = computed(() => selectionStore.selectedTraceMatrix);

const sourceType = computed(() => traceMatrix.value?.sourceType || "");
const targetType = computed(() => traceMatrix.value?.targetType || "");

const totalCount = computed(() => {
  const count = traceMatrix.value?.count || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

const generatedCount = computed(() => {
  const count = traceMatrix.value?.generatedCount || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

const approvedCount = computed(() => {
  const count = traceMatrix.value?.approvedCount || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

/**
 * Switches to tree view and highlights this type matrix.
 */
function handleViewLevel(): void {
  if (!traceMatrix.value) return;

  documentStore.addDocumentOfTypes([
    traceMatrix.value.sourceType,
    traceMatrix.value.targetType,
  ]);
}
</script>
