<template>
  <GenericStepperModal
    v-model="currentStep"
    :steps="steps"
    :isOpen="isOpen"
    :title="title"
    :isLoading="isLoading"
    size="l"
    @onClose="onClose"
    @onReset="clearData"
    @onSubmit="$emit('onSubmit')"
  >
    <template v-slot:items>
      <slot name="beforeItems" />

      <v-stepper-content :step="projectStep">
        <v-container class="pa-10">
          <ProjectSelector
            :isOpen="isOpen"
            @onProjectSelected="selectProject"
            @onProjectUnselected="unselectProject"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content :step="versionStep">
        <v-container class="pl-10 pr-10 pt-0 pb-0">
          <VersionSelector
            v-if="selectedProject !== undefined"
            :isOpen="isOpen"
            :project="selectedProject"
            @onVersionSelected="selectVersion"
            @onVersionUnselected="unselectVersion"
          />
        </v-container>
      </v-stepper-content>
      <slot name="afterItems" />
    </template>

    <template v-slot:action:main>
      <slot name="action:main" />
    </template>
  </GenericStepperModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericStepperModal from "@/components/common/generic/GenericStepperModal.vue";
import type {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
  StepState,
} from "@/types/common-components";
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import ProjectSelector from "@/components/project/selector/ProjectSelector.vue";
import VersionSelector from "@/components/project/version-selector/VersionSelector.vue";
import { versionToString } from "@/util/to-string";

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
      // TODO: Check if can delete
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
    beforeStepNames(): string[] {
      return this.beforeSteps.map((step) => step[0]);
    },
    afterStepNames(): string[] {
      return this.afterSteps.map((step) => step[0]);
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
