<template>
  <generic-stepper-modal
    v-model="currentStep"
    :steps="steps"
    :is-open="isOpen"
    :title="title"
    :is-loading="isLoading"
    size="l"
    @close="handleClose"
    @reset="clearData"
    @submit="$emit('submit')"
  >
    <template v-slot:items>
      <slot name="beforeItems" />

      <v-stepper-content :step="projectStep">
        <project-selector
          :is-open="projectSelectorIsOpen"
          @selected="selectProject"
          @unselected="unselectProject"
        />
      </v-stepper-content>

      <v-stepper-content :step="versionStep">
        <version-selector
          :is-open="versionSelectorIsOpen"
          :project="selectedProject"
          @selected="selectVersion"
          @unselected="unselectVersion"
        />
      </v-stepper-content>
      <slot name="afterItems" />
    </template>
  </generic-stepper-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
  StepState,
  ProjectIdentifier,
  ProjectVersion,
} from "@/types";
import { versionToString } from "@/util";
import { GenericStepperModal } from "@/components/common";
import { ProjectSelector } from "@/components/project/selector";
import VersionSelector from "./VersionSelector.vue";

const SELECT_PROJECT_DEFAULT_NAME = "Select a Project";
const SELECT_VERSION_DEFAULT_NAME = "Select a Version";

/**
 * Presents a stepper in a modal for selecting a project and version.
 *
 * @emits-1 `submit` - On submit.
 * @emits-2 `update:loading` (boolean) - On loading update.
 * @emits-3 `close` - On close.
 * @emits-4 `input` (number) - On step change.
 * @emits-5 `update:project` (string) - On project update.
 * @emits-6 `update:version` (string) - On version update.
 */
export default Vue.extend({
  name: "ProjectVersionStepperModal",
  components: {
    GenericStepperModal,
    ProjectSelector,
    VersionSelector,
  },
  props: {
    /**
     * The current step of the stepper.
     */
    value: {
      type: Number,
      default: 1,
    },
    title: {
      type: String,
      required: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    project: {
      type: Object as PropType<OptionalProjectIdentifier>,
      required: false,
    },
    version: {
      type: Object as PropType<OptionalProjectVersion>,
      required: false,
    },
    startStep: {
      type: Number,
      default: 1,
      required: false,
    },
    /**
     * The StepStates of the steps coming before selection a project.
     */
    beforeSteps: {
      type: Array as PropType<Array<StepState>>,
      required: false,
      default: () => [] as StepState[],
    },
    /**
     * The StepStates of the steps coming after selecting a version.
     */
    afterSteps: {
      type: Array as PropType<Array<StepState>>,
      required: false,
      default: () => [] as StepState[],
    },
  },
  data() {
    return {
      localSteps: [
        [SELECT_PROJECT_DEFAULT_NAME, false],
        [SELECT_VERSION_DEFAULT_NAME, false],
      ] as StepState[],
      fileSelectorOpen: false,
    };
  },
  methods: {
    /**
     * Clears all modal data.
     */
    clearData() {
      this.selectedProject = this.project;
      this.selectedVersion = undefined;
      this.fileSelectorOpen = false;
      this.currentStep = this.startStep;
      if (this.project?.name) {
        Vue.set(this.localSteps, 0, [this.project.name, true]);
      } else {
        Vue.set(this.localSteps, 0, [SELECT_PROJECT_DEFAULT_NAME, false]);
      }
      this.$emit("update:loading", false);
    },
    /**
     * Closes the modal.
     */
    handleClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.$emit("close");
    },
    /**
     * Selects a project.
     * @param project - The project to select
     * @param goToNextStep - If true, the step will be incremented.
     */
    selectProject(project: ProjectIdentifier, goToNextStep = false) {
      if (this.currentStep !== 1) return;

      this.selectedProject = project;

      Vue.set(this.localSteps, 0, [project.name, true]);

      if (goToNextStep) this.currentStep++;
    },
    /**
     * Deselects a project.
     */
    unselectProject() {
      this.selectedProject = undefined;
      Vue.set(this.localSteps, 0, [SELECT_PROJECT_DEFAULT_NAME, false]);
    },
    /**
     * Selects a version.
     * @param version - The version to select.
     */
    selectVersion(version: ProjectVersion) {
      this.selectedVersion = version;
      Vue.set(this.localSteps, 1, [versionToString(version), true]);
    },
    /**
     * Deselects a version.
     */
    unselectVersion() {
      this.selectedVersion = undefined;
      Vue.set(this.localSteps, 1, [SELECT_VERSION_DEFAULT_NAME, false]);
    },
  },
  computed: {
    /**
     * @return All steps.
     */
    steps(): StepState[] {
      return [...this.beforeSteps, ...this.localSteps, ...this.afterSteps];
    },
    /**
     * @return The current step, which emits updates on change.
     */
    currentStep: {
      get(): number {
        return this.value;
      },
      set(newStep: number): void {
        this.$emit("input", newStep);
      },
    },
    /**
     * @return The project step number.
     */
    projectStep(): number {
      return this.beforeSteps.length + 1;
    },
    /**
     * @return The version step number.
     */
    versionStep(): number {
      return this.projectStep + 1;
    },
    /**
     * @return The total steps.
     */
    totalSteps(): number {
      return (
        (this.beforeSteps?.length || 0) + 2 + (this.afterSteps?.length || 0)
      );
    },
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
          if (this.currentStep < this.projectStep) {
            return this.beforeSteps[this.currentStep][1];
          } else {
            const numberStepsBefore = this.beforeSteps.length + 2;
            const afterStepIndex = this.currentStep - numberStepsBefore - 1;
            return this.afterSteps[afterStepIndex][1];
          }
      }
    },
    /**
     * @return The selected project, which emits updates on change.
     */
    selectedProject: {
      get(): OptionalProjectIdentifier {
        return this.project;
      },
      set(newProject: OptionalProjectIdentifier): void {
        this.$emit("update:project", newProject);
      },
    },
    /**
     * @return The selected version, which emits updates on change.
     */
    selectedVersion: {
      get(): OptionalProjectVersion {
        return this.version;
      },
      set(newVersion: OptionalProjectVersion): void {
        this.$emit("update:version", newVersion);
      },
    },
    /**
     * @return Whether the selector is open to the project page.
     */
    projectSelectorIsOpen(): boolean {
      return this.isOpen && this.currentStep === this.projectStep;
    },
    /**
     * @return Whether the selector is open to the version page.
     */
    versionSelectorIsOpen(): boolean {
      return (
        this.isOpen &&
        this.selectedProject !== undefined &&
        this.currentStep === this.versionStep
      );
    },
  },
  watch: {
    /**
     * Clears modal data on open.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.clearData();
    },
  },
});
</script>
