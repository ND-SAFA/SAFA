<template>
  <div>
    <panel-card :title="targetArtifactsLabel" collapsable borderless>
      <template #title-actions>
        <text-button
          text
          small
          label="View Parents"
          icon="view-tree"
          @click="viewsStore.addDocumentOfTypes([targetType])"
        />
      </template>
      <artifact-list-display
        v-if="targetArtifacts.length > 0"
        :artifacts="targetArtifacts"
        data-cy="list-selected-parent-artifacts"
        item-data-cy="list-selected-parent-artifact-item"
        class="bg-background rounded"
        @click="viewsStore.addDocumentOfNeighborhood($event)"
      />
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>

    <panel-card :title="sourceArtifactsLabel" collapsable borderless>
      <template #title-actions>
        <text-button
          text
          small
          label="View Children"
          icon="view-tree"
          @click="viewsStore.addDocumentOfTypes([sourceType])"
        />
      </template>
      <artifact-list-display
        v-if="sourceArtifacts.length > 0"
        :artifacts="sourceArtifacts"
        data-cy="list-selected-child-artifacts"
        item-data-cy="list-selected-child-artifact-item"
        class="bg-background rounded"
        @click="viewsStore.addDocumentOfNeighborhood($event)"
      />
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no child artifacts."
      />
    </panel-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays parent and child artifacts in the selected trace matrix.
 */
export default {
  name: "TraceMatrixArtifacts",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { artifactStore, timStore, viewsStore } from "@/hooks";
import { PanelCard, Typography, TextButton } from "@/components/common";
import { ArtifactListDisplay } from "@/components/artifact/display";

const traceMatrix = computed(() => timStore.selectedTraceMatrix);

const sourceType = computed(() => traceMatrix.value?.sourceType || "");
const sourceArtifacts = computed(() =>
  artifactStore.getArtifactsByType(sourceType.value)
);
const sourceArtifactsLabel = computed(() =>
  sourceArtifacts.value.length === 1
    ? "1 Child Artifact"
    : `${sourceArtifacts.value.length} Child Artifacts`
);

const targetType = computed(() => traceMatrix.value?.targetType || "");
const targetArtifacts = computed(() =>
  artifactStore.getArtifactsByType(targetType.value)
);
const targetArtifactsLabel = computed(() =>
  targetArtifacts.value.length === 1
    ? "1 Parent Artifact"
    : `${targetArtifacts.value.length} Parent Artifacts`
);
</script>
