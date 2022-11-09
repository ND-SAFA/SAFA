<template>
  <v-container style="max-width: 40em">
    <typography
      el="p"
      value="Select files to upload to the current project version."
    />
    <project-files-input
      v-model="selectedFiles"
      data-cy="input-files-version"
      class="mx-2"
    />
    <generic-switch
      v-model="replaceAllArtifacts"
      label="Replace all artifacts"
      class="ml-4"
    />
    <v-btn block color="primary" @click="handleSubmit">
      Upload Project Files
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { IdentifierModel, VersionModel } from "@/types";
import { logStore, projectStore } from "@/hooks";
import { handleUploadProjectVersion } from "@/api";
import { GenericSwitch, Typography } from "@/components/common";
import { ProjectFilesInput } from "../base";

/**
 * Displays inputs for uploading a new version.
 */
export default Vue.extend({
  name: "UploadNewVersion",
  components: {
    Typography,
    GenericSwitch,
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
      selectedProject: undefined as IdentifierModel | undefined,
      selectedVersion: undefined as VersionModel | undefined,
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
      const currentProject = projectStore.project;
      const currentVersion = currentProject.projectVersion;

      if (!open || !currentProject.projectId) return;

      this.selectedProject = currentProject;
      this.selectedVersion = currentVersion;
      this.selectedFiles = [];
      this.replaceAllArtifacts = false;
    },
  },
  methods: {
    /**
     * Closes the modal and clears data.
     */
    handleReset() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.selectedFiles = [];
    },
    /**
     * Attempts to upload a new project version.
     */
    handleSubmit() {
      if (this.selectedProject === undefined) {
        return logStore.onWarning("No project is selected.");
      }
      if (this.selectedVersion === undefined) {
        return logStore.onWarning("No project version is selected.");
      }

      this.isLoading = true;

      handleUploadProjectVersion(
        this.selectedProject.projectId,
        this.selectedVersion.versionId,
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
