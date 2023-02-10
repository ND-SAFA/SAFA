<template>
  <div>
    <project-identifier-input
      v-model:name="identifier.name"
      v-model:description="identifier.description"
      :data-cy-name="dataCyName"
      :data-cy-description="dataCyDescription"
    />
    <v-container style="max-width: 40em">
      <switch-input
        v-model="emptyFiles"
        class="mt-0"
        label="Create an empty project"
        data-cy="toggle-create-empty-project"
      />
      <project-files-input
        v-if="!emptyFiles"
        v-model="selectedFiles"
        data-cy="input-files-bulk"
      />
      <v-btn
        block
        color="primary"
        :disabled="isDisabled"
        :loading="isLoading"
        data-cy="button-create-project"
        @click="handleCreate"
      >
        Create Project From Files
      </v-btn>
    </v-container>
  </div>
</template>

<script lang="ts">
/**
 * Creates projects with bulk uploaded files.
 */
export default {
  name: "ProjectFilesUploader",
};
</script>

<script setup lang="ts">
import { computed, ref, withDefaults, defineEmits, defineProps } from "vue";
import { identifierSaveStore } from "@/hooks";
import { handleBulkImportProject } from "@/api";
import { SwitchInput } from "@/components/common";
import ProjectFilesInput from "./ProjectFilesInput.vue";
import ProjectIdentifierInput from "./ProjectIdentifierInput.vue";

const props = withDefaults(
  defineProps<{
    dataCyName?: string;
    dataCyDescription?: string;
  }>(),
  {
    dataCyName: "input-project-name",
    dataCyDescription: "input-project-description",
  }
);

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const selectedFiles = ref<File[]>([]);
const isLoading = ref(false);
const emptyFiles = ref(false);

const identifier = computed(() => identifierSaveStore.editedIdentifier);

const isDisabled = computed(() => {
  const isNameInvalid = identifier.value.name.length === 0;

  if (emptyFiles.value) {
    return isNameInvalid;
  } else {
    return (
      isNameInvalid ||
      (selectedFiles.value.length === 0 && !emptyFiles.value) ||
      !selectedFiles.value.find(({ name }) => name === "tim.json")
    );
  }
});

/**
 * Attempts to save the project.
 */
async function handleCreate() {
  isLoading.value = true;

  handleBulkImportProject(identifier.value, selectedFiles.value, {
    onSuccess: () => {
      selectedFiles.value = [];
      isLoading.value = false;
      emit("submit");
    },
    onError: () => {
      isLoading.value = false;
    },
  });
}
</script>
