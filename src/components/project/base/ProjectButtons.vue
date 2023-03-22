<template>
  <flex-box v-if="doDisplay" wrap t="2" class="settings-buttons">
    <text-button
      text
      label="Download"
      icon="download"
      data-cy="button-settings-download"
      @click="handleDownload"
    />
    <text-button
      text
      label="Edit"
      icon="edit"
      data-cy="button-settings-edit"
      @click="handleEdit"
    />
    <separator vertical />
    <text-button
      text
      label="Delete"
      icon="delete"
      data-cy="button-settings-delete"
      @click="handleDelete"
    />
    <project-identifier-modal
      :open="isEditOpen"
      @close="isEditOpen = false"
      @save="isEditOpen = false"
    />
    <confirm-project-delete
      :open="isDeleteOpen"
      @close="isDeleteOpen = false"
      @confirm="isDeleteOpen = false"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays buttons for interacting with projects.
 */
export default {
  name: "ProjectButtons",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { identifierSaveStore, projectStore, sessionStore } from "@/hooks";
import { handleDownloadProjectCSV } from "@/api";
import { FlexBox, TextButton, Separator } from "@/components/common";
import ProjectIdentifierModal from "./ProjectIdentifierModal.vue";
import ConfirmProjectDelete from "./ConfirmProjectDelete.vue";

const isEditOpen = ref(false);
const isDeleteOpen = ref(false);

const doDisplay = computed(() => sessionStore.isEditor(projectStore.project));

/**
 * Opens the edit modal.
 */
function handleEdit(): void {
  identifierSaveStore.baseIdentifier = projectStore.project;
  isEditOpen.value = true;
}

/**
 * Opens the edit modal.
 */
function handleDelete(): void {
  identifierSaveStore.baseIdentifier = projectStore.project;
  isDeleteOpen.value = true;
}

/**
 * Downloads project files
 */
function handleDownload(): void {
  handleDownloadProjectCSV();
}
</script>
