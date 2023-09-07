<template>
  <modal
    size="md"
    :loading="projectApiStore.saveProjectLoading"
    :open="open"
    :title="modalTitle"
    data-cy="modal-project-edit"
    @close="handleClose"
  >
    <save-project-inputs @save="handleClose" />
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
import { computed } from "vue";
import { projectApiStore, identifierSaveStore, appStore } from "@/hooks";
import { Modal } from "@/components/common";
import SaveProjectInputs from "./SaveProjectInputs.vue";

const open = computed(() => appStore.popups.saveProject);
const isUpdate = computed(() => identifierSaveStore.isUpdate);
const modalTitle = computed(() =>
  isUpdate.value ? "Edit Project" : "Create Project"
);

/**
 * Closes the save project panel.
 */
function handleClose(): void {
  appStore.close("saveProject");
}
</script>
