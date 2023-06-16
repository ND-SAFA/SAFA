<template>
  <modal
    size="md"
    :loading="projectApiStore.saveProjectLoading"
    :open="props.open"
    :title="modalTitle"
    data-cy="modal-project-edit"
    @close="handleCancel"
  >
    <project-files-uploader
      v-if="showUpload"
      data-cy-name="input-project-name-modal"
      data-cy-description="input-project-description-modal"
      @submit="handleCancel"
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
  name: "ProjectIdentifierModal",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { projectApiStore, identifierSaveStore } from "@/hooks";
import { Modal, TextButton } from "@/components/common";
import ProjectFilesUploader from "./ProjectFilesUploader.vue";
import ProjectIdentifierInput from "./ProjectIdentifierInput.vue";

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "save"): void;
}>();

const identifier = computed(() => identifierSaveStore.editedIdentifier);
const isUpdate = computed(() => identifierSaveStore.isUpdate);
const showUpload = computed(() => !identifierSaveStore.isUpdate);
const canSave = computed(() => identifierSaveStore.canSave);
const modalTitle = computed(() =>
  isUpdate.value ? "Edit Project" : "Create Project"
);

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    identifierSaveStore.resetIdentifier();
  }
);

/**
 * Cancels the project saving.
 */
function handleCancel(): void {
  emit("close");
}

/**
 * Confirms the project saving.
 */
function handleSave(): void {
  projectApiStore.handleSave({
    onSuccess: () => emit("save"),
  });
}
</script>
