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
    @submit="$emit('onSubmit')"
  >
    <template v-slot:items>
      <slot name="beforeItems" />

      <v-stepper-content :step="projectStep">
        <project-selector
          :is-open="isOpen"
          @onProjectSelected="selectProject"
          @onProjectUnselected="unselectProject"
        />
      </v-stepper-content>

      <v-stepper-content :step="versionStep">
        <version-selector
          v-if="selectedProject !== undefined"
          :is-open="isOpen"
          :project="selectedProject"
          @onVersionSelected="selectVersion"
          @onVersionUnselected="unselectVersion"
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

export default Vue.extend({
  name: "project-version-stepper-modal",
  components: {
    GenericStepperModal,
    ProjectSelector,
    VersionSelector,
  },
  props: {
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
    beforeSteps: {
      type: Array as PropType<Array<StepState>>,
      required: false,
      default: () => [] as StepState[],
    },
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
    clearData() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.fileSelectorOpen = false;
      this.currentStep = 1;
      this.$emit("update:isLoading", false);
    },
    onClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.$emit("onClose");
    },

    selectProject(project: ProjectIdentifier) {
      this.selectedProject = project;
      this.currentStep++;
      Vue.set(this.localSteps, 0, [project.name, true]);
    },
    unselectProject() {
      this.selectedProject = undefined;
      Vue.set(this.localSteps, 0, [SELECT_PROJECT_DEFAULT_NAME, false]);
    },
    selectVersion(version: ProjectVersion) {
      this.selectedVersion = version;
      Vue.set(this.localSteps, 1, [versionToString(version), true]);
      if (this.versionStep < this.totalSteps) {
        this.currentStep++;
      }
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
