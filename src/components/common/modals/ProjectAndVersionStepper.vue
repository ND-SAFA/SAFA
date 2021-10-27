<template>
  <v-container>
    <v-stepper v-model="currentStep" alt-labels>
      <v-stepper-header>
        <template v-for="(stepName, stepIndex) in stepNames">
          <v-stepper-step
            :complete="currentStep > stepIndex + 1"
            :step="stepIndex + 1"
            :key="stepIndex"
          >
            {{ stepName }}
          </v-stepper-step>
          <v-divider
            :key="`${stepName}-divider`"
            v-if="stepIndex < stepNames.length - 1"
          />
        </template>
      </v-stepper-header>

      <v-stepper-items>
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
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script lang="ts">
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import ProjectSelector from "@/components/common/ProjectSelector.vue";
import VersionSelector from "@/components/common/modals/VersionSelector.vue";
import Vue, { PropType } from "vue";
import {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
} from "@/types/common-components";
import { versionToString } from "@/util/to-string";

const SELECT_PROJECT_DEFAULT_NAME = "Select a Project";
const SELECT_VERSION_DEFAULT_NAME = "Select a Version";

export default Vue.extend({
  name: "ProjectAndVersionStepper",
  components: {
    ProjectSelector,
    VersionSelector,
  },
  data() {
    return {
      currentSteps: [SELECT_PROJECT_DEFAULT_NAME, SELECT_VERSION_DEFAULT_NAME],
    };
  },
  props: {
    beforeSteps: {
      type: Array as PropType<Array<string>>,
      required: false,
      default: () => [] as string[],
    },
    afterSteps: {
      type: Array as PropType<Array<string>>,
      required: false,
      default: () => [] as string[],
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    selectedProject: {
      type: Object as PropType<OptionalProjectIdentifier>,
    },
    selectedVersion: {
      type: Object as PropType<OptionalProjectVersion>,
    },
    value: {
      type: Number,
      required: true,
    },
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.currentSteps = [
          SELECT_PROJECT_DEFAULT_NAME,
          SELECT_VERSION_DEFAULT_NAME,
        ];
      }
    },
  },
  computed: {
    stepNames(): string[] {
      return this.beforeSteps.concat(this.currentSteps.concat(this.afterSteps));
    },
    currentStep: {
      get(): number {
        return this.value;
      },
      set(value: number): void {
        this.$emit("input", value);
      },
    },
    project: {
      get(): OptionalProjectIdentifier {
        return this.selectedProject;
      },
      set(newProject: OptionalProjectIdentifier): void {
        this.$emit("update:selectedProject", newProject);
      },
    },
    projectVersion: {
      get(): OptionalProjectVersion {
        return this.selectedVersion;
      },
      set(newVersion: OptionalProjectVersion): void {
        this.$emit("update:selectedVersion", newVersion);
      },
    },
    projectStep(): number {
      return this.beforeSteps.length + 1;
    },
    versionStep(): number {
      return this.projectStep + 1;
    },
    totalSteps(): number {
      return this.stepNames.length;
    },
  },
  methods: {
    selectProject(project: ProjectIdentifier) {
      this.project = project;
      this.currentStep++;
      Vue.set(this.currentSteps, 0, project.name);
    },
    unselectProject() {
      this.project = undefined;
      Vue.set(this.currentSteps, 0, SELECT_PROJECT_DEFAULT_NAME);
    },
    selectVersion(version: ProjectVersion) {
      this.projectVersion = version;
      Vue.set(this.currentSteps, 1, versionToString(version));
      if (this.versionStep < this.totalSteps) {
        this.currentStep++;
      }
    },
    unselectVersion() {
      this.projectVersion = undefined;
      Vue.set(this.currentSteps, 1, SELECT_VERSION_DEFAULT_NAME);
    },
  },
});
</script>
