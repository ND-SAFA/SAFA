<template>
  <panel-card subtitle="Select files to upload to the current project version.">
    <project-files-input v-model="files" data-cy="input-files-version" />
    <switch-input v-model="replaceAllArtifacts" label="Replace all artifacts" />
    <template #actions>
      <text-button
        block
        :disabled="!files || files.length === 0"
        label="Upload Project Files"
        color="primary"
        data-cy="button-upload-files"
        @click="handleSubmit"
      />
    </template>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays inputs for uploading a new version.
 */
export default {
  name: "UploadNewVersion",
};
</script>

<script setup lang="ts">
import { ref, watch } from "vue";
import { OpenableProps } from "@/types";
import { createVersionApiStore, projectStore } from "@/hooks";
import { SwitchInput, PanelCard, TextButton } from "@/components/common";
import { ProjectFilesInput } from "@/components/project/save";

const props = defineProps<OpenableProps>();

const files = ref<File[]>([]);
const replaceAllArtifacts = ref(false);

/**
 * Resets component data.
 */
function handleReset() {
  createVersionApiStore.handleReset();
  files.value = [];
  replaceAllArtifacts.value = false;
}

/**
 * Uploads a new project version.
 */
function handleSubmit() {
  createVersionApiStore
    .handleImport(
      projectStore.projectId,
      projectStore.versionId,
      files.value,
      true,
      replaceAllArtifacts.value
    )
    .then(() => handleReset());
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReset();
  }
);
</script>
