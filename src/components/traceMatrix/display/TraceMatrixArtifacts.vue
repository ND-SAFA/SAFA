<template>
  <div>
    <panel-card :title="targetArtifactsLabel" collapsable>
      <template #title-actions>
        <text-button
          text
          label="View Parents"
          icon="view-tree"
          @click="documentStore.addDocumentOfTypes([targetType])"
        />
      </template>
      <list
        v-if="targetArtifacts.length > 0"
        :scroll-height="300"
        data-cy="list-selected-parent-artifacts"
      >
        <list-item
          v-for="artifact in targetArtifacts"
          :key="artifact.id"
          clickable
          :action-cols="1"
          data-cy="list-selected--parent-artifact-item"
          @click="documentStore.addDocumentOfNeighborhood(artifact)"
        >
          <artifact-body-display display-title :artifact="artifact" />
        </list-item>
      </list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>

    <panel-card :title="sourceArtifactsLabel" collapsable>
      <template #title-actions>
        <text-button
          text
          label="View Children"
          icon="view-tree"
          @click="documentStore.addDocumentOfTypes([sourceType])"
        />
      </template>
      <list
        v-if="sourceArtifacts.length > 0"
        :scroll-height="300"
        data-cy="list-selected-child-artifacts"
      >
        <list-item
          v-for="artifact in sourceArtifacts"
          :key="artifact.id"
          clickable
          :action-cols="1"
          data-cy="list-selected--child-artifact-item"
          @click="documentStore.addDocumentOfNeighborhood(artifact)"
        >
          <artifact-body-display display-title :artifact="artifact" />
        </list-item>
      </list>
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
import { artifactStore, documentStore, selectionStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  TextButton,
  ListItem,
  ArtifactBodyDisplay,
  List,
} from "@/components/common";

const traceMatrix = computed(() => selectionStore.selectedTraceMatrix);

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
