<template>
  <panel-card
    v-if="artifacts.length > 0"
    :title="artifactsLabel"
    collapsable
    borderless
  >
    <template #title-actions>
      <text-button
        text
        small
        label="View Artifacts"
        icon="view-tree"
        @click="viewsStore.addDocumentOfTypes([name])"
      />
    </template>
    <artifact-list-display
      :artifacts="artifacts"
      data-cy="list-selected-artifacts"
      item-data-cy="list-selected-artifact-item"
      class="bg-background rounded"
      @click="viewsStore.addDocumentOfNeighborhood($event)"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the list of artifacts within the selected artifact level.
 */
export default {
  name: "ArtifactLevelArtifacts",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { artifactStore, viewsStore, timStore } from "@/hooks";
import { PanelCard, TextButton } from "@/components/common";
import { ArtifactListDisplay } from "@/components/artifact/display";

const artifactLevel = computed(() => timStore.selectedArtifactLevel);
const name = computed(() => artifactLevel.value?.name || "");

const artifacts = computed(() => artifactStore.getArtifactsByType(name.value));
const artifactsLabel = computed(() =>
  artifacts.value.length === 1
    ? "1 Artifact"
    : `${artifacts.value.length} Artifacts`
);
</script>
