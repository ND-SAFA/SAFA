<template>
  <details-panel panel="displayArtifactLevel" data-cy="panel-artifact-type">
    <flex-box v-if="displayActions" b="2">
      <text-button
        text
        label="View Artifacts"
        icon="view-tree"
        @click="handleViewLevel"
      />
    </flex-box>

    <panel-card>
      <flex-box align="center" justify="between">
        <div class="overflow-hidden">
          <typography
            ellipsis
            variant="subtitle"
            el="h1"
            :value="name"
            data-cy="text-selected-name"
          />
          <q-tooltip>{{ name }}</q-tooltip>
        </div>
        <icon :id="iconId" size="md" color="primary" />
      </flex-box>

      <separator b="2" />

      <typography variant="caption" value="Details" />
      <typography el="p" :value="countDisplay" />
    </panel-card>

    <panel-card
      v-if="artifactLevel"
      title="Type Options"
      data-cy="panel-artifact-type-options"
    >
      <type-direction-input :artifact-type="artifactLevel" />
      <type-icon-input :artifact-type="artifactLevel" />
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
import {
  timStore,
  documentStore,
  projectStore,
  selectionStore,
  sessionStore,
} from "@/hooks";
import {
  PanelCard,
  Typography,
  TypeDirectionInput,
  TypeIconInput,
  Icon,
  DetailsPanel,
  FlexBox,
  TextButton,
  Separator,
} from "@/components/common";

const displayActions = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const artifactLevel = computed(() => selectionStore.selectedArtifactLevel);

const name = computed(() => artifactLevel.value?.name || "");

const countDisplay = computed(() => {
  const count = artifactLevel.value?.count || 0;

  return count === 1 ? "1 Artifact" : `${count} Artifacts`;
});

const iconId = computed(() => timStore.getTypeIcon(name.value));

/**
 * Switches to tree view and highlights this artifact level.
 */
function handleViewLevel(): void {
  if (!artifactLevel.value) return;

  documentStore.addDocumentOfTypes([artifactLevel.value.name]);
}
</script>
