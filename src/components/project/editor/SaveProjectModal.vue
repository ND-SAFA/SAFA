<template>
  <modal
    size="md"
    :loading="projectApiStore.saveProjectLoading"
    :open="open"
    :title="modalTitle"
    data-cy="modal-project-edit"
    @close="handleClose"
  >
    <project-files-uploader
      v-if="showUpload"
      data-cy-name="input-project-name-modal"
      data-cy-description="input-project-description-modal"
      @submit="handleClose"
    />
    <project-identifier-input
      v-else
      v-model:name="identifier.name"
      v-model:description="identifier.description"
      data-cy-name="input-project-name-modal"
      data-cy-description="input-project-description-modal"
    />
    <template v-if="!showUpload" #actions>
      <text-button
        color="primary"
        label="Save"
        :disabled="!canSave"
        data-cy="button-project-save"
        @click="handleSave"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for creating or editing a project.
 */
export default {
  name: "SaveProjectModal",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { PanelType } from "@/types";
import {
  projectApiStore,
  identifierSaveStore,
  appStore,
  getProjectApiStore,
} from "@/hooks";
import { Modal, TextButton } from "@/components/common";
import { ProjectFilesUploader, ProjectIdentifierInput } from "../base";

const open = computed(() => appStore.isProjectCreatorOpen);
const identifier = computed(() => identifierSaveStore.editedIdentifier);
const isUpdate = computed(() => identifierSaveStore.isUpdate);
const showUpload = computed(() => !identifierSaveStore.isUpdate);
const canSave = computed(() => identifierSaveStore.canSave);
const modalTitle = computed(() =>
  isUpdate.value ? "Edit Project" : "Create Project"
);

watch(
  () => open.value,
  (open) => {
    if (!open) return;

    identifierSaveStore.resetIdentifier();
  }
);

/**
 * Closes the save project panel.
 */
function handleClose(): void {
  appStore.closePanel(PanelType.projectSaver);
}

/**
 * Saves the project being edited.
 */
function handleSave(): void {
  projectApiStore.handleSave({
    onSuccess: async () => {
      handleClose();

      await getProjectApiStore.handleReload();
    },
  });
}
</script>
