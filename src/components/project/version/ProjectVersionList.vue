<template>
  <generic-stepper
    minimal
    v-model="currentStep"
    :steps="steps"
    @submit="handleSubmit"
  >
    <template v-slot:items>
      <v-stepper-content :step="projectStep">
        <project-selector
          minimal
          :is-open="projectSelectorIsOpen"
          @selected="selectProject"
          @unselected="unselectProject"
        />
      </v-stepper-content>

      <v-stepper-content :step="versionStep">
        <version-selector
          minimal
          :is-open="versionSelectorIsOpen"
          :project="selectedProject"
          @selected="selectVersion"
          @unselected="unselectVersion"
        />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
  StepState,
  IdentifierModel,
  VersionModel,
} from "@/types";
import { versionToString } from "@/util";
import { GenericStepper } from "@/components/common";
import { ProjectSelector } from "@/components/project/selector";
import VersionSelector from "./VersionSelector.vue";
import { handleLoadVersion } from "@/api";
import { logModule } from "@/store";

const SELECT_PROJECT_DEFAULT_NAME = "Select a Project";
const SELECT_VERSION_DEFAULT_NAME = "Select a Version";

/**
 * Presents a stepper in a modal for selecting a project and version.
 */
export default Vue.extend({
  name: "ProjectVersionStepperModal",
  components: {
    GenericStepper,
    ProjectSelector,
    VersionSelector,
  },
  data() {
    return {
      isLoading: false,
      currentStep: 1,
      startStep: 1,
      projectStep: 1,
      versionStep: 2,
      selectedProject: undefined as OptionalProjectIdentifier,
      selectedVersion: undefined as OptionalProjectVersion,
      steps: [
        [SELECT_PROJECT_DEFAULT_NAME, false],
        [SELECT_VERSION_DEFAULT_NAME, false],
      ] as StepState[],
    };
  },
  methods: {
    /**
     * Clears all modal data.
     */
    clearData() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.currentStep = this.startStep;
    },
    /**
     * Selects a project.
     * @param project - The project to select
     * @param goToNextStep - If true, the step will be incremented.
     */
    selectProject(project: IdentifierModel, goToNextStep = false) {
      if (this.currentStep !== 1) return;

      this.selectedProject = project;

      Vue.set(this.steps, 0, [project.name, true]);

      if (goToNextStep) this.currentStep++;
    },
    /**
     * Deselects a project.
     */
    unselectProject() {
      this.selectedProject = undefined;
      Vue.set(this.steps, 0, [SELECT_PROJECT_DEFAULT_NAME, false]);
    },
    /**
     * Selects a version.
     * @param version - The version to select.
     */
    selectVersion(version: VersionModel) {
      this.selectedVersion = version;
      Vue.set(this.steps, 1, [versionToString(version), true]);
    },
    /**
     * Deselects a version.
     */
    unselectVersion() {
      this.selectedVersion = undefined;
      Vue.set(this.steps, 1, [SELECT_VERSION_DEFAULT_NAME, false]);
    },
    /**
     * Submits a project version to load.
     */
    async handleSubmit(): Promise<void> {
      if (this.selectedProject === undefined) {
        logModule.onWarning("Please select a project to update.");
      } else if (this.selectedVersion === undefined) {
        logModule.onWarning("Please select a baseline version.");
      } else {
        this.isLoading = true;

        await handleLoadVersion(this.selectedVersion.versionId);

        this.isLoading = false;
        this.$emit("close");
      }
    },
  },
  computed: {
    /**
     * @return Whether the current step is done.
     */
    isStepDone(): boolean {
      switch (this.currentStep) {
        case this.projectStep:
          return this.selectedProject !== undefined;
        case this.versionStep:
          return this.selectedVersion !== undefined;
        default:
          return false;
      }
    },
    /**
     * @return Whether the selector is open to the project page.
     */
    projectSelectorIsOpen(): boolean {
      return this.currentStep === this.projectStep;
    },
    /**
     * @return Whether the selector is open to the version page.
     */
    versionSelectorIsOpen(): boolean {
      return (
        this.selectedProject !== undefined &&
        this.currentStep === this.versionStep
      );
    },
  },
});
</script>
