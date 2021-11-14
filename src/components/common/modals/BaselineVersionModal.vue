<template>
  <project-version-stepper-modal
    v-model="currentStep"
    :title="title"
    :isOpen="isOpen"
    :startStep="startStep"
    v-bind:isLoading.sync="isLoading"
    v-bind:project.sync="selectedProject"
    v-bind:version.sync="selectedVersion"
    @onSubmit="onSubmit"
    @onClose="$emit('onClose')"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier, ProjectVersion } from "@/types";
import { getProjectVersion } from "@/api";
import { appModule, projectModule } from "@/store";
import ProjectVersionStepperModal from "./ProjectVersionStepperModal.vue";

/**
 * Stepper for setting the current project and version.
 *
 * @emits `onClose` - Emitted when modal is exited or project + version set.
 */
export default Vue.extend({
  name: "baseline-version-modal",
  components: {
    ProjectVersionStepperModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
    startStep: {
      type: Number,
      default: 1,
      required: false,
    },
    title: {
      type: String,
      default: "Select Baseline Project Version",
    },
  },
  data() {
    return {
      isLoading: false,
      selectedVersion: undefined as ProjectVersion | undefined,
      currentStep: this.startStep,
      selectedProject: this.project,
    };
  },
  watch: {
    /**
     * Overrides selectedProject with the project prop.
     *
     * @param newProject - The new project prop.
     */
    project(newProject: ProjectIdentifier): void {
      this.selectedProject = newProject;
    },
  },
  methods: {
    onSubmit() {
      if (this.selectedProject === undefined) {
        appModule.onWarning("Please select a project to update.");
      } else if (this.selectedVersion === undefined) {
        appModule.onWarning("Please select a baseline version.");
      } else {
        this.isLoading = true;

        getProjectVersion(this.selectedVersion.versionId)
          .then(projectModule.setProjectCreationResponse)
          .finally(() => {
            this.isLoading = false;
            this.$emit("onClose");
          });
      }
    },
  },
});
</script>
