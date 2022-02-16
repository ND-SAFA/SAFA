<template>
  <project-version-stepper-modal
    v-model="currentStep"
    title="Upload Flat Files"
    :is-open="isOpen"
    :startStep="startStep"
    :after-steps="[['Upload Files', filesSelected.length > 0]]"
    v-bind:isLoading.sync="isLoading"
    v-bind:project.sync="selectedProject"
    v-bind:version.sync="selectedVersion"
    @submit="onSubmit"
    @close="onClose"
  >
    <template v-slot:afterItems>
      <v-stepper-content step="3">
        <generic-file-selector
          v-if="selectedVersion !== undefined"
          @change:files="onChangeFiles"
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
import { uploadNewProjectVersion } from "@/api";
import { GenericFileSelector } from "@/components/common/generic";
import ProjectVersionStepperModal from "./ProjectVersionStepperModal.vue";
import { projectModule } from "@/store";

/**
 * Modal for uploading a new version.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "upload-new-version-modal",
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
      filesSelected: [] as File[],
      isLoading: false,
      setAsNewVersion: true,
    };
  },
  watch: {
    isOpen(open: boolean) {
      const currentProject = projectModule.getProject;
      const currentVersion = currentProject.projectVersion;
      if (open && currentProject.projectId) {
        this.selectedProject = currentProject;

        if (currentVersion?.versionId) {
          this.selectedVersion = currentVersion;
        }
      }
    },
  },
  computed: {
    startStep(): number {
      return this.selectedProject === undefined ? 1 : 2;
    },
  },
  methods: {
    onClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.filesSelected = [];
      this.$emit("close");
    },
    onChangeFiles(files: File[]) {
      this.filesSelected = files;
    },
    onSubmit() {
      uploadNewProjectVersion(
        this.selectedProject,
        this.selectedVersion,
        this.filesSelected,
        this.setAsNewVersion,
        () => (this.isLoading = true),
        () => (this.isLoading = false),
        this.onClose
      );
    },
  },
});
</script>
