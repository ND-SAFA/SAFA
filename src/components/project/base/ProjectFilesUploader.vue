<template>
  <div>
    <project-identifier-input
      v-model:name="identifier.name"
      v-model:description="identifier.description"
      :data-cy-name="props.dataCyName"
      :data-cy-description="props.dataCyDescription"
    />
    <div style="max-width: 40em" class="q-mx-auto">
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
      <text-button
        block
        label="Create Project From Files"
        color="primary"
        :disabled="disabled"
        :loading="loading"
        class="q-mt-md"
        data-cy="button-create-project"
        @click="handleCreate"
      />
    </div>
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
import { computed, ref, withDefaults } from "vue";
import { identifierSaveStore } from "@/hooks";
import { handleBulkImportProject } from "@/api";
import { SwitchInput, TextButton } from "@/components/common";
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
const loading = ref(false);
const emptyFiles = ref(false);

const identifier = computed(() => identifierSaveStore.editedIdentifier);

const disabled = computed(() => {
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
  loading.value = true;

  handleBulkImportProject(identifier.value, selectedFiles.value, {
    onSuccess: () => {
      selectedFiles.value = [];
      loading.value = false;
      emit("submit");
    },
    onError: () => {
      loading.value = false;
    },
  });
}
</script>
