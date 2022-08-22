<template>
  <project-version-stepper-modal
    v-model="currentStep"
    title="Upload Flat Files"
    :is-open="isOpen"
    :startStep="startStep"
    :after-steps="[['Upload Files', selectedFiles.length > 0]]"
    v-bind:isLoading.sync="isLoading"
    v-bind:project.sync="selectedProject"
    v-bind:version.sync="selectedVersion"
    data-cy="modal-version-upload"
    @submit="onSubmit"
    @close="handleClose"
  >
    <template v-slot:afterItems>
      <v-stepper-content step="3">
        <generic-file-selector
          v-if="selectedVersion !== undefined"
          v-model="selectedFiles"
          data-cy="input-files-version"
        />
        <v-switch
          v-model="replaceAllArtifacts"
          label="Replace all artifacts"
          class="ml-1"
        />
      </v-stepper-content>
    </template>
  </project-version-stepper-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { IdentifierModel, VersionModel } from "@/types";
import { projectModule } from "@/store";
import { logStore } from "@/hooks";
import { handleUploadProjectVersion } from "@/api";
import { GenericFileSelector } from "@/components/common";
import ProjectVersionStepperModal from "./ProjectVersionStepperModal.vue";

/**
 * Modal for uploading a new version.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "UploadNewVersionModal",
  components: {
    GenericFileSelector,
    ProjectVersionStepperModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      currentStep: 1,
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
      const currentProject = projectModule.getProject;
      const currentVersion = currentProject.projectVersion;

      if (!open || !currentProject.projectId) return;

      this.selectedProject = currentProject;
      this.currentStep = 2;

      if (!currentVersion?.versionId) return;

      this.selectedVersion = currentVersion;
    },
  },
  computed: {
    /**
     * @return The start step, which skips the first step if a project is already selected.
     */
    startStep(): number {
      return this.selectedProject === undefined ? 1 : 2;
    },
  },
  methods: {
    /**
     * Closes the modal and clears data.
     */
    handleClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.selectedFiles = [];
      this.$emit("close");
    },
    /**
     * Attempts to upload a new project version.
     */
    onSubmit() {
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
        .then(() => this.handleClose())
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
