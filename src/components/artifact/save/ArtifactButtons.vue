<template>
  <div v-if="artifact">
    <flex-box>
      <text-button
        v-if="ENABLED_FEATURES.NASA_ARTIFACT_FLAG"
        text
        label="Flag"
        icon="flag"
        data-cy="button-artifact-flag"
        @click="handleFlag"
      />
      <text-button
        v-if="ENABLED_FEATURES.NASA_ARTIFACT_COMMENT"
        text
        label="Comment"
        icon="comment"
        data-cy="button-artifact-comment"
        @click="handleComment"
      />
      <text-button
        v-if="displayActions"
        text
        label="Edit"
        icon="edit"
        data-cy="button-artifact-edit"
        @click="artifactSaveStore.openPanel({})"
      />
      <text-button
        v-if="displayActions"
        text
        :loading="artifactApiStore.deleteLoading"
        label="Delete"
        icon="delete"
        data-cy="button-artifact-delete"
        @click="artifactApiStore.handleDelete(artifact)"
      />
    </flex-box>
    <flex-box justify="end">
      <text-button
        text
        label="Tree"
        icon="view-tree"
        data-cy="button-artifact-tree"
        @click="viewsStore.addDocumentOfNeighborhood(artifact)"
      />
      <text-button
        text
        label="Expand"
        icon="code"
        data-cy="button-artifact-body"
        @click="appStore.openDetailsPanel('displayArtifactBody')"
      />
    </flex-box>
  </div>
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
import { ENABLED_FEATURES } from "@/util";
import {
  appStore,
  artifactApiStore,
  artifactSaveStore,
  artifactStore,
  permissionStore,
  viewsStore,
} from "@/hooks";
import { FlexBox, TextButton } from "@/components/common";

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const artifact = computed(() => artifactStore.selectedArtifact);

function handleComment() {
  // TODO
}

function handleFlag() {
  // TODO
}
</script>
