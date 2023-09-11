<template>
  <panel-card v-if="artifacts.length > 0" :title="artifactsLabel" collapsable>
    <template #title-actions>
      <text-button
        text
        label="View Artifacts"
        icon="view-tree"
        @click="documentStore.addDocumentOfTypes([name])"
      />
    </template>
    <list :scroll-height="300" data-cy="list-selected-artifacts">
      <list-item
        v-for="artifact in artifacts"
        :key="artifact.id"
        clickable
        :action-cols="1"
        data-cy="list-selected-artifact-item"
        @click="documentStore.addDocumentOfNeighborhood(artifact)"
      >
        <artifact-body-display display-title :artifact="artifact" />
      </list-item>
    </list>
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
import { documentStore, selectionStore, artifactStore } from "@/hooks";
import { PanelCard, TextButton, List, ListItem } from "@/components/common";
import { ArtifactBodyDisplay } from "@/components/artifact/display";

const artifactLevel = computed(() => selectionStore.selectedArtifactLevel);
const name = computed(() => artifactLevel.value?.name || "");

const artifacts = computed(() => artifactStore.getArtifactsByType(name.value));
const artifactsLabel = computed(() =>
  artifacts.value.length === 1
    ? "1 Artifact"
    : `${artifacts.value.length} Artifacts`
);
</script>
