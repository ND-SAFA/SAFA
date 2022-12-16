<template>
  <v-container>
    <typography t="4" el="h1" variant="title" value="Open Project" />
    <v-divider />
    <typography el="p" y="2" value="Select a project and version to load." />
    <stepper
      v-model="currentStep"
      :steps="steps"
      :is-open="true"
      title="Select Project"
      :is-loading="isLoading"
      size="l"
      data-cy="project-version-stepper"
      @submit="handleSubmit"
    >
      <template v-slot:items>
        <v-stepper-content step="1">
          <project-selector
            :is-open="projectSelectorIsOpen"
            @selected="selectProject"
            @unselected="unselectProject"
          />
        </v-stepper-content>

        <v-stepper-content step="2">
          <version-selector
            :is-open="versionSelectorIsOpen"
            :project="selectedProject"
            @selected="selectVersion"
            @unselected="unselectVersion"
          />
        </v-stepper-content>
      </template>
    </stepper>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
  StepState,
  IdentifierSchema,
  VersionSchema,
} from "@/types";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { handleLoadVersion } from "@/api";
import { Stepper, Typography } from "@/components/common";
import ProjectSelector from "./ProjectSelector.vue";
import VersionSelector from "./VersionSelector.vue";

const SELECT_PROJECT_DEFAULT_NAME = "Select a Project";
const SELECT_VERSION_DEFAULT_NAME = "Select a Version";

/**
 * Presents a stepper in a modal for selecting a project and version.
 */
export default Vue.extend({
  name: "ProjectVersionStepper",
  components: {
    Stepper,
    ProjectSelector,
    VersionSelector,
    Typography,
  },
  data() {
    return {
      currentStep: 1,
      steps: [
        [SELECT_PROJECT_DEFAULT_NAME, false],
        [SELECT_VERSION_DEFAULT_NAME, false],
      ] as StepState[],
      isLoading: false,
      selectedProject: undefined as OptionalProjectIdentifier,
      selectedVersion: undefined as OptionalProjectVersion,
    };
  },
  computed: {
    /**
     * @return Whether the current step is done.
     */
    isStepDone(): boolean {
      return this.currentStep === 2
        ? this.selectedVersion !== undefined
        : this.selectedProject !== undefined;
    },
    /**
     * @return Whether the selector is open to the project page.
     */
    projectSelectorIsOpen(): boolean {
      return this.currentStep === 1;
    },
    /**
     * @return Whether the selector is open to the version page.
     */
    versionSelectorIsOpen(): boolean {
      return this.currentStep === 2;
    },
  },
  methods: {
    /**
     * Clears all modal data.
     */
    clearData() {
      this.selectedProject = projectStore.project;
      this.selectedVersion = undefined;
      this.currentStep = 1;

      if (this.selectedProject?.name) {
        Vue.set(this.steps, 0, [this.selectedProject.name, true]);
      } else {
        Vue.set(this.steps, 0, [SELECT_PROJECT_DEFAULT_NAME, false]);
      }
    },
    /**
     * Closes the modal.
     */
    handleClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
    },
    /**
     * Selects a project.
     * @param project - The project to select
     * @param goToNextStep - If true, the step will be incremented.
     */
    selectProject(project: IdentifierSchema, goToNextStep = false) {
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
    selectVersion(version: VersionSchema) {
      this.selectedVersion = version;
      Vue.set(this.steps, 1, [versionToString(version), true]);
      this.handleSubmit();
    },
    /**
     * Deselects a version.
     */
    unselectVersion() {
      this.selectedVersion = undefined;
      Vue.set(this.steps, 1, [SELECT_VERSION_DEFAULT_NAME, false]);
    },
    /**
     * Loads the selected project.
     */
    async handleSubmit(): Promise<void> {
      if (!this.selectedProject || !this.selectedVersion) return;

      this.isLoading = true;

      await handleLoadVersion(this.selectedVersion.versionId);

      this.isLoading = false;
    },
  },
});
</script>
