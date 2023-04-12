<template>
  <flex-box full-width justify="between">
    <text-button
      v-if="isUpdate"
      text
      label="Delete"
      icon="delete"
      data-cy="button-artifact-delete"
      @click="handleDelete"
    />
    <q-space />
    <text-button
      :loading="loading"
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
import { computed, ref } from "vue";
import { appStore, artifactSaveStore, selectionStore } from "@/hooks";
import { handleDeleteArtifact, handleSaveArtifact } from "@/api";
import { TextButton, FlexBox } from "@/components/common";

const loading = ref(false);

const canSave = computed(() => artifactSaveStore.canSave);
const isUpdate = computed(() => artifactSaveStore.isUpdate);

/**
 * Attempts to delete the selected artifact.
 */
function handleDelete(): void {
  const artifact = selectionStore.selectedArtifact;
  if (!artifact) return;

  handleDeleteArtifact(artifact, {
    onSuccess: () => appStore.closeSidePanels(),
  });
}

/**
 * Attempts to save the artifact.
 */
function handleSubmit(): void {
  loading.value = true;

  handleSaveArtifact(
    artifactSaveStore.finalizedArtifact,
    artifactSaveStore.isUpdate,
    artifactSaveStore.parentArtifact,
    {
      onSuccess: () => appStore.openDetailsPanel("displayArtifact"),
      onComplete: () => (loading.value = false),
    }
  );
}
</script>
