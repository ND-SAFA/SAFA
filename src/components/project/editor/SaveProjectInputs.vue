<template>
  <div>
    <project-files-uploader
      v-if="!isUpdate"
      data-cy-name="input-project-name-modal"
      data-cy-description="input-project-description-modal"
      @submit="emit('save')"
    />
    <project-identifier-input
      v-else
      v-model:name="identifier.name"
      v-model:description="identifier.description"
      is-update
      data-cy-name="input-project-name-modal"
      data-cy-description="input-project-description-modal"
    />
    <flex-box full-width justify="end">
      <text-button
        v-if="isUpdate"
        color="primary"
        label="Save"
        :disabled="!canSave"
        :loading="loading"
        data-cy="button-project-save"
        @click="handleSave"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Inputs for creating or editing a project.
 */
export default {
  name: "SaveProjectInputs",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  projectApiStore,
  identifierSaveStore,
  getProjectApiStore,
} from "@/hooks";
import { TextButton, FlexBox } from "@/components/common";
import {
  ProjectFilesUploader,
  ProjectIdentifierInput,
} from "@/components/project/save";

const emit = defineEmits<{
  (e: "save"): void;
}>();

const identifier = computed(() => identifierSaveStore.editedIdentifier);
const isUpdate = computed(() => identifierSaveStore.isUpdate);
const canSave = computed(() => identifierSaveStore.canSave);
const loading = computed(() => projectApiStore.saveProjectLoading);

/**
 * Saves the project being edited.
 */
function handleSave(): void {
  projectApiStore.handleSave({
    onSuccess: async () => {
      emit("save");

      await getProjectApiStore.handleLoadProjects();
    },
  });
}
</script>
