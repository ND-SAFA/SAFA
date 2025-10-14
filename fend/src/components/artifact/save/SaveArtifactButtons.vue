<template>
  <flex-box full-width justify="between">
    <text-button
      v-if="isUpdate"
      text
      :loading="artifactApiStore.deleteLoading"
      label="Delete"
      icon="delete"
      data-cy="button-artifact-delete"
      @click="handleDelete"
    />
    <q-space />
    <text-button
      :loading="artifactApiStore.saveLoading"
      :disabled="!canSave"
      label="Save"
      icon="save"
      data-cy="button-artifact-save"
      @click="handleSubmit"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Buttons for deleting and saving an edited artifact.
 */
export default {
  name: "SaveArtifactButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  appStore,
  artifactApiStore,
  artifactSaveStore,
  artifactStore,
} from "@/hooks";
import { TextButton, FlexBox } from "@/components/common";

const canSave = computed(() => artifactSaveStore.canSave);
const isUpdate = computed(() => artifactSaveStore.isUpdate);

/**
 * Attempts to delete the selected artifact.
 */
function handleDelete(): void {
  const artifact = artifactStore.selectedArtifact;

  if (!artifact) return;

  artifactApiStore.handleDelete(artifact, {
    onSuccess: () => appStore.closeSidePanels(),
  });
}

/**
 * Attempts to save the artifact.
 */
function handleSubmit(): void {
  artifactApiStore.handleSave(
    artifactSaveStore.finalizedArtifact,
    artifactSaveStore.isUpdate,
    artifactSaveStore.parentArtifacts,
    artifactSaveStore.childArtifacts,
    {
      onSuccess: () => appStore.openDetailsPanel("displayArtifact"),
    }
  );
}
</script>
