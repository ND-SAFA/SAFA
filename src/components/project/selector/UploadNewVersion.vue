<template>
  <panel-card title="Data File Upload">
    <typography
      el="p"
      value="Select files to upload to the current project version."
    />
    <project-files-input v-model="files" data-cy="input-files-version" />
    <switch-input
      v-model="replaceAllArtifacts"
      label="Replace all artifacts"
      class="ml-4"
    />
    <template #actions>
      <text-button
        block
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
import { projectStore } from "@/hooks";
import { handleUploadProjectVersion } from "@/api";
import {
  SwitchInput,
  Typography,
  PanelCard,
  TextButton,
} from "@/components/common";
import { ProjectFilesInput } from "../base";

const props = defineProps<{
  open: boolean;
}>();

const files = ref<File[]>([]);
const loading = ref(false);
const replaceAllArtifacts = ref(false);

/**
 * Resets component data.
 */
function handleReset() {
  files.value = [];
  loading.value = false;
  replaceAllArtifacts.value = false;
}

/**
 * Uploads a new project version.
 */
function handleSubmit() {
  loading.value = true;

  handleUploadProjectVersion(
    projectStore.projectId,
    projectStore.versionId,
    files.value,
    true,
    replaceAllArtifacts.value
  )
    .then(() => handleReset())
    .finally(() => (loading.value = false));
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReset();
  }
);
</script>
