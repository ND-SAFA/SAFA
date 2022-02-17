<template>
  <generic-stepper-modal
    v-model="currentStep"
    :steps="steps"
    :is-open="isOpen"
    :title="title"
    :is-loading="isLoading"
    size="l"
    @close="onClose"
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
import { GenericStepperModal } from "@/components/common/generic";
import { ProjectSelector } from "@/components/project/selector";
import { VersionSelector } from "@/components/project/version-selector";

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
  name: "project-version-stepper-modal",
  components: {
    GenericStepperModal,
    ProjectSelector,
    VersionSelector,
  },
  props: {
    /**
     * The current step of the stepper, used as the v-model value.
     * @model
     */
    value: {
      type: Number,
      default: 1,
    },
    /**
     * The title of the modal
     */
    title: {
      type: String,
      required: true,
    },
    /**
     *  Whether this current modal is open and in view.
     */
    isOpen: {
      type: Boolean,
      required: true,
    },
    /**
     * Whether the current modal is loading.
     */
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    /**
     * The project used to bind and synchronize with parent.
     */
    project: {
      type: Object as PropType<OptionalProjectIdentifier>,
      required: false,
    },
    /**
     * The version used to bind and synchronize with parent.
     */
    version: {
      type: Object as PropType<OptionalProjectVersion>,
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
    /**
     * Defines the starting step in the stepper. Useful if project or versions is
     * already selected.
     */
    startStep: {
      type: Number,
      default: 1,
      required: false,
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
    onClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.$emit("close");
    },
    selectProject(project: ProjectIdentifier, goToNextStep = false) {
      if (this.currentStep === 1) {
        this.selectedProject = project;

        Vue.set(this.localSteps, 0, [project.name, true]);

        if (goToNextStep) this.currentStep++;
      }
    },
    unselectProject() {
      this.selectedProject = undefined;
      Vue.set(this.localSteps, 0, [SELECT_PROJECT_DEFAULT_NAME, false]);
    },
    selectVersion(version: ProjectVersion) {
      this.selectedVersion = version;
      Vue.set(this.localSteps, 1, [versionToString(version), true]);
    },
    unselectVersion() {
      this.selectedVersion = undefined;
      Vue.set(this.localSteps, 1, [SELECT_VERSION_DEFAULT_NAME, false]);
    },
  },
  computed: {
    steps(): StepState[] {
      return this.beforeSteps.concat(this.localSteps.concat(this.afterSteps));
    },
    currentStep: {
      get(): number {
        return this.value;
      },
      set(newStep: number): void {
        this.$emit("input", newStep);
      },
    },
    selectedProject: {
      get(): OptionalProjectIdentifier {
        return this.project;
      },
      set(newProject: OptionalProjectIdentifier): void {
        this.$emit("update:project", newProject);
      },
    },
    selectedVersion: {
      get(): OptionalProjectVersion {
        return this.version;
      },
      set(newVersion: OptionalProjectVersion): void {
        this.$emit("update:version", newVersion);
      },
    },
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
    projectStep(): number {
      return this.beforeSteps.length + 1;
    },
    versionStep(): number {
      return this.projectStep + 1;
    },
    totalSteps(): number {
      return this.beforeSteps.length + 2 + this.afterSteps.length;
    },
    projectSelectorIsOpen(): boolean {
      return this.isOpen && this.currentStep === this.projectStep;
    },
    versionSelectorIsOpen(): boolean {
      return (
        this.isOpen &&
        this.selectedProject !== undefined &&
        this.currentStep === this.versionStep
      );
    },
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
  },
});
</script>
