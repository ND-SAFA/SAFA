<template>
  <div>
    <panel-card v-for="(matrix, idx) in model" :key="idx" class="q-my-md">
      <flex-box full-width align="center">
        <flex-box column full-width>
          <flex-box full-width b="2">
            <artifact-type-input
              v-model="matrix.source"
              show-count
              label="Child Type"
              class="q-mr-md width-50"
            />
            <artifact-type-input
              v-model="matrix.target"
              show-count
              label="Parent Type"
              class="width-50"
            />
          </flex-box>
          <flex-box full-width justify="center">
            <attribute-chip
              v-for="detail in getMatrixDetails(matrix)"
              :key="detail"
              :value="detail"
              icon="trace"
            />
          </flex-box>
        </flex-box>
        <icon-button
          icon="delete"
          color="negative"
          tooltip="Remove trace matrix"
          class="q-ml-md"
          @click="handleRemoveMatrix(idx)"
        />
      </flex-box>
    </panel-card>

    <flex-box justify="center">
      <text-button
        text
        label="Add New Matrix"
        icon="add"
        @click="handleCreateMatrix"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Creates an array of trace matrices.
 */
export default {
  name: "TraceMatrixCreator",
};
</script>

<script setup lang="ts">
import { MatrixSchema, TraceMatrixCreatorProps } from "@/types";
import { artifactStore, traceStore, useVModel } from "@/hooks";
import {
  ArtifactTypeInput,
  FlexBox,
  IconButton,
  AttributeChip,
  TextButton,
  PanelCard,
} from "@/components/common";

const props = defineProps<TraceMatrixCreatorProps>();

defineEmits<{
  (e: "update:modelValue", value: MatrixSchema[]): void;
}>();

const model = useVModel(props, "modelValue");

/**
 * Returns displayable characteristics on a matrix of artifacts.
 * @param matrix - The matrix to get details for.
 */
function getMatrixDetails(matrix: MatrixSchema): string[] {
  const sources = artifactStore.getArtifactsByType(matrix.source) || [];
  const targets = artifactStore.getArtifactsByType(matrix.target) || [];
  const manual = traceStore.getTraceLinksByArtifactSets(sources, targets, [
    "manual",
  ]);
  const approved = traceStore.getTraceLinksByArtifactSets(sources, targets, [
    "approved",
  ]);

  return [
    manual.length === 1 ? "1 Manual Link" : `${manual.length} Manual Links`,
    approved.length === 1
      ? "1 Approved Link"
      : `${approved.length} Approved Links`,
  ];
}

/**
 * Creates a new trace matrix.
 */
function handleCreateMatrix(): void {
  model.value.push({ source: "", target: "" });
}

/**
 * Removes a matrix from the list.
 * @param idx - The matrix index to remove.
 */
function handleRemoveMatrix(idx: number) {
  model.value = model.value.filter(
    (_: MatrixSchema, currentIdx: number) => currentIdx !== idx
  );
}
</script>
