<template>
  <div>
    <v-card
      v-for="(matrix, idx) in model"
      :key="idx"
      outlined
      class="my-2 pa-2 primary-border"
    >
      <flex-box full-width align="center">
        <flex-box column full-width>
          <flex-box b="2">
            <artifact-type-input
              v-model="matrix.source"
              hide-details
              label="Source Type"
              class="mr-2"
              style="width: 50%"
            />
            <artifact-type-input
              v-model="matrix.target"
              hide-details
              label="Target Type"
              class="mr-2"
              style="width: 50%"
            />
          </flex-box>
          <flex-box justify="center">
            <attribute-chip
              v-for="(detail, detailIdx) in getMatrixDetails(matrix)"
              :key="detail"
              :value="detail"
              :icon="
                detailIdx < 2
                  ? 'mdi-alpha-a-box-outline'
                  : 'mdi-ray-start-arrow'
              "
            />
          </flex-box>
        </flex-box>
        <icon-button
          icon-id="mdi-delete-outline"
          color="error"
          tooltip="Remove trace matrix"
          @click="handleRemoveMatrix(idx)"
        />
      </flex-box>
    </v-card>

    <flex-box justify="center">
      <text-button text variant="add" @click="handleCreateMatrix">
        Add New Matrix
      </text-button>
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
import { defineEmits, defineProps } from "vue";
import { ArtifactLevelSchema } from "@/types";
import { artifactStore, traceStore, useVModel } from "@/hooks";
import {
  ArtifactTypeInput,
  FlexBox,
  IconButton,
  AttributeChip,
  TextButton,
} from "@/components/common";

const props = defineProps<{
  modelValue: ArtifactLevelSchema[];
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: ArtifactLevelSchema[]): void;
}>();

const model = useVModel(props, "modelValue");

/**
 * Returns displayable characteristics on a matrix of artifacts.
 * @param matrix - The matrix to get details for.
 */
function getMatrixDetails(matrix: ArtifactLevelSchema): string[] {
  const sources = artifactStore.getArtifactsByType[matrix.source] || [];
  const targets = artifactStore.getArtifactsByType[matrix.target] || [];
  const manual = traceStore.getTraceLinksByArtifactSets(sources, targets, [
    "manual",
  ]);
  const approved = traceStore.getTraceLinksByArtifactSets(sources, targets, [
    "approved",
  ]);

  return [
    `Source Artifacts: ${sources.length}`,
    `Target Artifacts: ${targets.length}`,
    `Manual Links: ${manual.length}`,
    `Approved Links: ${approved.length}`,
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
    (_: ArtifactLevelSchema, currentIdx: number) => currentIdx !== idx
  );
}
</script>
