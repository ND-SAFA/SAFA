<template>
  <flex-box b="2">
    <text-button
      text
      label="View Content"
      icon="code"
      data-cy="button-artifact-body"
      @click="handleViewBody"
    />
    <text-button
      v-if="displayActions"
      text
      label="Edit"
      icon="edit"
      data-cy="button-artifact-edit"
      @click="handleEdit"
    />
    <separator vertical />
    <text-button
      v-if="displayActions"
      text
      :loading="artifactApiStore.deleteLoading"
      label="Delete"
      icon="delete"
      data-cy="button-artifact-delete"
      @click="handleDelete"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays artifact buttons.
 */
export default {
  name: "ArtifactButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  appStore,
  artifactApiStore,
  permissionStore,
  selectionStore,
} from "@/hooks";
import { FlexBox, TextButton, Separator } from "@/components/common";

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const artifact = computed(() => selectionStore.selectedArtifact);

/**
 * Attempts to delete the selected artifact.
 */
function handleDelete(): void {
  if (!artifact.value) return;

  artifactApiStore.handleDelete(artifact.value, {
    onSuccess: () => appStore.closeSidePanels(),
  });
}

/**
 * Opens the artifact creator.
 */
function handleEdit(): void {
  appStore.openArtifactCreatorTo({});
}

/**
 * Opens the artifact body display.
 */
function handleViewBody(): void {
  appStore.openDetailsPanel("displayArtifactBody");
}
</script>
