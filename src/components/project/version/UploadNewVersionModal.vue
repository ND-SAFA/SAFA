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
    @submit="onSubmit"
    @close="handleClose"
  >
    <template v-slot:afterItems>
      <v-stepper-content step="3">
        <generic-file-selector
          v-if="selectedVersion !== undefined"
          @change:files="handleChangeFiles"
        />
      </v-stepper-content>
    </template>

    <template v-slot:action:main>
      <v-checkbox
        v-if="currentStep === 3"
        v-model="setAsNewVersion"
        color="secondary"
      >
        <template v-slot:label>
          <label style="color: black" class="ma-0 pa-0">
            Set as current version
          </label>
        </template>
      </v-checkbox>
    </template>
  </project-version-stepper-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectIdentifier, ProjectVersion } from "@/types";
import { logModule, projectModule } from "@/store";
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
      selectedProject: undefined as ProjectIdentifier | undefined,
      selectedVersion: undefined as ProjectVersion | undefined,
      selectedFiles: [] as File[],
      isLoading: false,
      setAsNewVersion: true,
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
     * Updates the selected files.
     * @param files - The files to select.
     */
    handleChangeFiles(files: File[]) {
      this.selectedFiles = files;
    },
    /**
     * Attempts to upload a new project version.
     */
    onSubmit() {
      if (this.selectedProject === undefined) {
        return logModule.onWarning("No project is selected.");
      }
      if (this.selectedVersion === undefined) {
        return logModule.onWarning("No project version is selected.");
      }

      this.isLoading = true;

      handleUploadProjectVersion(
        this.selectedProject.projectId,
        this.selectedVersion.versionId,
        this.selectedFiles,
        this.setAsNewVersion
      )
        .then(() => this.handleClose())
        .finally(() => (this.isLoading = false));
    },
  },
});
</script>
