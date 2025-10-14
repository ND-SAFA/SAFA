<template>
  <flex-box v-if="permissionStore.isAllowed('project.edit_data')">
    <text-button text icon="delete" label="Delete" @click="handleDelete" />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays trace matrix action buttons.
 */
export default {
  name: "TraceMatrixButtons",
};
</script>

<script setup lang="ts">
import { permissionStore, timStore, traceMatrixApiStore } from "@/hooks";
import { FlexBox, TextButton } from "@/components/common";

/**
 * Attempts to delete the selected trace matrix.
 */
function handleDelete(): void {
  const traceMatrix = timStore.selectedTraceMatrix;

  if (!traceMatrix) return;

  traceMatrixApiStore.handleDeleteTypes(
    traceMatrix.sourceType,
    traceMatrix.targetType
  );
}
</script>
