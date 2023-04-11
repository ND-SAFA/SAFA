<template>
  <details-panel panel="displayArtifactLevel">
    <flex-box b="2">
      <text-button
        text
        label="View In Tree"
        icon="artifact"
        @click="handleViewLevel"
      />
    </flex-box>

    <panel-card :title="artifactLevelName" data-cy="panel-artifact-type">
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
import { layoutStore, selectionStore, typeOptionsStore } from "@/hooks";
import {
  PanelCard,
  Typography,
  TypeDirectionInput,
  TypeIconInput,
  TextButton,
  Icon,
  FlexBox,
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

/**
 * Switches to tree view and highlights this type level.
 */
function handleViewLevel(): void {
  if (!artifactLevel.value) return;

  layoutStore.viewTreeTypes([artifactLevel.value.name]);
}
</script>
