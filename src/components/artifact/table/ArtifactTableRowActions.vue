<template>
  <flex-box>
    <icon-button
      icon="view-tree"
      :tooltip="`View artifacts related to '${artifact.name}'`"
      data-cy="button-artifact-tree-icon"
      @click="handleOpenTree"
    />
    <icon-button
      v-if="displayActions"
      icon="trace"
      :rotate="-90"
      :tooltip="`Add parent to '${artifact.name}'`"
      data-cy="button-artifact-parent-icon"
      @click="handleLinkParent"
    />
    <icon-button
      v-if="displayActions"
      icon="trace"
      :rotate="90"
      :tooltip="`Add child to '${artifact.name}'`"
      data-cy="button-artifact-child-icon"
      @click="handleLinkChild"
    />
    <icon-button
      v-if="displayActions"
      icon="edit"
      :tooltip="`Edit '${artifact.name}'`"
      data-cy="button-artifact-edit-icon"
      @click="handleEdit"
    />
    <icon-button
      v-if="displayActions"
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
import { computed } from "vue";
import { ArtifactProps } from "@/types";
import {
  artifactApiStore,
  artifactSaveStore,
  layoutStore,
  permissionStore,
  traceSaveStore,
  viewsStore,
} from "@/hooks";
import { FlexBox, IconButton } from "@/components/common";

const props = defineProps<ArtifactProps>();

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

/**
 * Opens the edit artifact window.
 */
function handleEdit() {
  artifactSaveStore.openPanel({
    artifact: props.artifact,
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
  viewsStore.addDocumentOfNeighborhood(props.artifact);
  layoutStore.mode = "tree";
}

/**
 * Opens the create trace link panel with this artifact as the child.
 */
function handleLinkParent(): void {
  traceSaveStore.openPanel({
    type: "source",
    artifactId: props.artifact.id,
  });
}

/**
 * Opens the create trace link panel with this artifact as the parent.
 */
function handleLinkChild(): void {
  traceSaveStore.openPanel({
    type: "target",
    artifactId: props.artifact.id,
  });
}
</script>
