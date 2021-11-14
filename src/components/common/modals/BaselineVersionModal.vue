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

const PROJECT_SELECTION_STEP = 1;
const VERSION_SELECTION_STEP = 2;

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
    /**
     * Whether the current component should be in open.
     */
    isOpen: {
      type: Boolean,
      required: true,
    },
    /**
     * The title of the modal encapsulating this component.
     */
    title: {
      type: String,
      default: "Select Baseline Project Version",
    },
    /**
     * Optional project which if defined begins the stepper on version selection
     * fetching the versions of given project.
     */
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
  },
  data() {
    return {
      currentStep:
        this.project === undefined
          ? PROJECT_SELECTION_STEP
          : VERSION_SELECTION_STEP,
      selectedVersion: undefined as ProjectVersion | undefined,
      selectedProject: this.project,
      isLoading: false,
    };
  },
  computed: {
    startStep(): number {
      return this.project === undefined
        ? PROJECT_SELECTION_STEP
        : VERSION_SELECTION_STEP;
    },
  },
  watch: {
    /**
     * If project property changes to defined project then selected project
     * is set and stepper is advanced to version selection step.
     *
     * @param newProject - The new project prop.
     */
    project(newProject: ProjectIdentifier | undefined): void {
      if (newProject !== undefined) {
        this.selectedProject = newProject;
        this.currentStep = VERSION_SELECTION_STEP;
      }
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
