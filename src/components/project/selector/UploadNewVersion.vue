<template>
  <panel-card>
    <typography el="h2" variant="subtitle" value="Data File Upload" />
    <typography
      el="p"
      value="Select files to upload to the current project version."
    />
    <project-files-input
      v-model="selectedFiles"
      data-cy="input-files-version"
    />
    <switch-input
      v-model="replaceAllArtifacts"
      label="Replace all artifacts"
      class="ml-4"
    />
    <v-btn
      block
      color="primary"
      data-cy="button-upload-files"
      @click="handleSubmit"
    >
      Upload Project Files
    </v-btn>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { projectStore } from "@/hooks";
import { handleUploadProjectVersion } from "@/api";
import { SwitchInput, Typography, PanelCard } from "@/components/common";
import { ProjectFilesInput } from "../base";

/**
 * Displays inputs for uploading a new version.
 */
export default Vue.extend({
  name: "UploadNewVersion",
  components: {
    PanelCard,
    Typography,
    SwitchInput,
    ProjectFilesInput,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      selectedFiles: [] as File[],
      isLoading: false,
      setAsNewVersion: true,
      replaceAllArtifacts: false,
    };
  },
  watch: {
    /**
     * Sets the current project and version when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.selectedFiles = [];
      this.replaceAllArtifacts = false;
    },
  },
  methods: {
    /**
     * Closes the modal and clears data.
     */
    handleReset() {
      this.selectedFiles = [];
    },
    /**
     * Attempts to upload a new project version.
     */
    handleSubmit() {
      this.isLoading = true;

      handleUploadProjectVersion(
        projectStore.projectId,
        projectStore.versionId,
        this.selectedFiles,
        this.setAsNewVersion,
        this.replaceAllArtifacts
      )
        .then(() => this.handleReset())
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
