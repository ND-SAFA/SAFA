<template>
  <details-panel panel="displayTraceMatrix">
    <template #actions>
      <trace-matrix-buttons />
    </template>
    <trace-matrix-content />
    <trace-matrix-traces />
    <trace-matrix-artifacts />
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
import { DetailsPanel } from "@/components/common";
import {
  TraceMatrixContent,
  TraceMatrixTraces,
  TraceMatrixArtifacts,
} from "@/components/traceMatrix/display";
import { TraceMatrixButtons } from "@/components/traceMatrix/save";
</script>
