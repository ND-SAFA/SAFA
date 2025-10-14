<template>
  <div>
    <project-identifier-input
      v-model:name="identifier.name"
      v-model:description="identifier.description"
      :is-update="isUpdate"
      :data-cy-name="props.dataCyName"
      :data-cy-description="props.dataCyDescription"
    />
    <div class="q-mx-auto long-input">
      <project-files-input
        v-if="!emptyFiles"
        v-model="selectedFiles"
        data-cy="input-files-bulk"
      />
      <switch-input
        v-model="emptyFiles"
        label="Create an empty project"
        data-cy="toggle-create-empty-project"
      />
      <br />
      <switch-input
        v-model="summarize"
        label="Generate artifact summaries"
        data-cy="toggle-create-summarize"
      />
      <text-button
        block
        label="Create Project From Files"
        color="primary"
        :disabled="disabled"
        :loading="createProjectApiStore.loading"
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
import { ProjectIdentifierProps } from "@/types";
import { createProjectApiStore, identifierSaveStore } from "@/hooks";
import { SwitchInput, TextButton } from "@/components/common";
import ProjectFilesInput from "./ProjectFilesInput.vue";
import ProjectIdentifierInput from "./ProjectIdentifierInput.vue";

const props = withDefaults(
  defineProps<
    Pick<ProjectIdentifierProps, "dataCyName" | "dataCyDescription">
  >(),
  {
    dataCyName: "input-project-name",
    dataCyDescription: "input-project-description",
  }
);

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const selectedFiles = ref<File[]>([]);
const emptyFiles = ref(false);
const summarize = ref(false);

const identifier = computed(() => identifierSaveStore.editedIdentifier);
const isUpdate = computed(() => identifierSaveStore.isUpdate);

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
  await createProjectApiStore.handleBulkImport(
    identifier.value,
    selectedFiles.value,
    summarize.value,
    {
      onSuccess: () => {
        selectedFiles.value = [];
        identifierSaveStore.resetIdentifier(true);
        emit("submit");
      },
    }
  );
}
</script>
