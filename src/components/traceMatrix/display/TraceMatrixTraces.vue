<template>
  <panel-card :title="traceLabel" collapsable borderless>
    <template #title-actions>
      <text-button
        text
        small
        label="View Artifacts"
        icon="view-tree"
        @click="handleViewLevel"
      />
    </template>
    <flex-box>
      <flex-item parts="6">
        <typography variant="caption" value="Generated Trace Links" />
        <typography el="p" :value="generatedCount" />
        <typography variant="caption" value="Approved Trace Links" />
        <typography el="p" :value="approvedCount" />
      </flex-item>
      <flex-item parts="6">
        <typography variant="caption" value="Trace Coverage" />
        <flex-box align="center">
          <attribute-chip :value="traceCoverage.percentage" confidence-score />
          <typography el="span" :value="traceCoverage.text" l="1" />
        </flex-box>
      </flex-item>
    </flex-box>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays information about trace links in the selected matrix.
 */
export default {
  name: "TraceMatrixTraces",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { artifactStore, subtreeStore, timStore, viewsStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  TextButton,
  FlexBox,
  FlexItem,
  AttributeChip,
} from "@/components/common";

const traceMatrix = computed(() => timStore.selectedTraceMatrix);

const sourceType = computed(() => traceMatrix.value?.sourceType || "");
const targetType = computed(() => traceMatrix.value?.targetType || "");

const traceLabel = computed(() => {
  const count = traceMatrix.value?.count || 0;

  return count === 1 ? "1 Trace Link" : `${count} Trace Links`;
});

const generatedCount = computed(() => traceMatrix.value?.generatedCount || 0);

const approvedCount = computed(() => traceMatrix.value?.approvedCount || 0);

/**
 * Calculate the percentage of child artifacts of this type
 * that trace to at least one parent artifact of this type.
 */
const traceCoverage = computed(() => {
  const sourceArtifacts = artifactStore.allArtifacts.filter(
    (artifact) => artifact.type === sourceType.value
  );
  const sourceCount = sourceArtifacts.length;
  const traceCount = sourceArtifacts
    .map(({ id }) => subtreeStore.getParents(id))
    .filter((parents) =>
      parents.some(
        (id) => artifactStore.getArtifactById(id)?.type === targetType.value
      )
    ).length;
  const coverage = traceCount / sourceCount;

  return {
    text: `(${traceCount}/${sourceCount})`,
    percentage: coverage,
  };
});

/**
 * Switches to tree view and highlights this type matrix.
 */
function handleViewLevel(): void {
  if (!traceMatrix.value) return;

  viewsStore.addDocumentOfTypes([
    traceMatrix.value.sourceType,
    traceMatrix.value.targetType,
  ]);
}
</script>
