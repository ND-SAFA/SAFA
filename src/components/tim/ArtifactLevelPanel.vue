<template>
  <details-panel panel="displayArtifactLevel" data-cy="panel-artifact-type">
    <panel-card :title="artifactLevelName">
      <template #title-actions>
        <icon :id="iconId" size="md" color="primary" />
      </template>
      <typography variant="caption" value="Details" />
      <typography el="p" :value="countDisplay" />
    </panel-card>

    <panel-card
      v-if="artifactLevel"
      title="Type Options"
      data-cy="panel-artifact-type-options"
    >
      <type-direction-input :artifact-level="artifactLevel" />
      <type-icon-input :artifact-level="artifactLevel" />
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact level information.
 */
export default {
  name: "ArtifactLevelPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { selectionStore, typeOptionsStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  TypeDirectionInput,
  TypeIconInput,
  Icon,
  DetailsPanel,
} from "@/components/common";

const artifactLevel = computed(() => selectionStore.selectedArtifactLevel);
const artifactLevelName = computed(() => artifactLevel.value?.name || "");

const countDisplay = computed(() => {
  const count = artifactLevel.value?.count || 0;

  return count === 1 ? "1 Artifact" : `${count} Artifacts`;
});

const iconId = computed(() =>
  typeOptionsStore.getArtifactTypeIcon(artifactLevelName.value)
);
</script>
