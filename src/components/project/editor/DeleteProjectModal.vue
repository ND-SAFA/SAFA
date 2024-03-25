<template>
  <modal
    :loading="projectApiStore.deleteProjectLoading"
    :open="open"
    title="Delete Project"
    subtitle="Are you sure you want to delete this project? Type in the project's name to confirm deletion."
    data-cy="modal-project-delete"
    @close="handleClose"
  >
    <text-input
      v-model="confirmText"
      :label="label"
      data-cy="input-project-delete-name"
    />
    <template #actions>
      <text-button
        color="negative"
        label="Delete"
        :disabled="!canDelete"
        :loading="projectApiStore.deleteProjectLoading"
        data-cy="button-project-delete"
        @click="handleConfirm"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for confirming project deletion.
 */
export default {
  name: "DeleteProjectModal",
};
</script>

<script setup lang="ts">
import { ref, computed } from "vue";
import { projectApiStore, identifierSaveStore, appStore } from "@/hooks";
import { Modal, TextInput, TextButton } from "@/components/common";

const confirmText = ref("");

const open = computed(() => appStore.popups.deleteProject);
const projectName = computed(
  () => identifierSaveStore.baseIdentifier?.name || ""
);
const label = computed(() => `Type "${projectName.value}"`);
const canDelete = computed(() => confirmText.value === projectName.value);

/**
 * Clears the modal data and closes the modal.
 */
function handleClose(): void {
  confirmText.value = "";
  appStore.close("deleteProject");
}

/**
 * Confirms the project deletion.
 */
function handleConfirm(): void {
  projectApiStore.handleDelete({
    onSuccess: handleClose,
  });
}
</script>
