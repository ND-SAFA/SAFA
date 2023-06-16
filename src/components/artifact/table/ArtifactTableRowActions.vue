<template>
  <flex-box>
    <icon-button
      icon="edit"
      :tooltip="`Edit '${artifact.name}'`"
      data-cy="button-artifact-edit-icon"
      @click="handleEdit"
    />
    <icon-button
      icon="delete"
      :tooltip="`Delete '${artifact.name}'`"
      data-cy="button-artifact-delete-icon"
      @click="handleDelete"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Represents actions for an artifact.
 */
export default {
  name: "ArtifactTableRowActions",
};
</script>

<script setup lang="ts">
import { ArtifactSchema } from "@/types";
import { appStore, artifactApiStore, selectionStore } from "@/hooks";
import { FlexBox, IconButton } from "@/components/common";

const props = defineProps<{
  artifact: ArtifactSchema;
}>();

/**
 * Opens the edit artifact window.
 */
function handleEdit() {
  selectionStore.selectArtifact(props.artifact.id);
  appStore.openArtifactCreatorTo({
    isNewArtifact: false,
  });
}

/**
 * Opens the delete artifact window.
 */
function handleDelete() {
  artifactApiStore.handleDelete(props.artifact);
}
</script>
