<template>
  <flex-box>
    <icon-button
      icon="view-tree"
      :tooltip="`View artifacts related to '${artifact.name}'`"
      data-cy="button-artifact-tree-icon"
      @click="handleOpenTree"
    />
    <icon-button
      icon="trace"
      :rotate="-90"
      :tooltip="`Add parent to '${artifact.name}'`"
      data-cy="button-artifact-parent-icon"
      @click="handleLinkParent"
    />
    <icon-button
      icon="trace"
      :rotate="90"
      :tooltip="`Add child to '${artifact.name}'`"
      data-cy="button-artifact-child-icon"
      @click="handleLinkChild"
    />
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
import { ArtifactSchema, GraphMode } from "@/types";
import {
  appStore,
  artifactApiStore,
  documentStore,
  layoutStore,
  selectionStore,
} from "@/hooks";
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

/**
 * Opens tree view with the current artifact selected.
 */
function handleOpenTree(): void {
  documentStore.addDocumentOfNeighborhood(props.artifact);
  layoutStore.mode = GraphMode.tree;
}

/**
 * Opens the create trace link panel with this artifact as the child.
 */
function handleLinkParent(): void {
  appStore.openTraceCreatorTo({
    type: "source",
    artifactId: props.artifact.id,
  });
}

/**
 * Opens the create trace link panel with this artifact as the parent.
 */
function handleLinkChild(): void {
  appStore.openTraceCreatorTo({
    type: "target",
    artifactId: props.artifact.id,
  });
}
</script>
