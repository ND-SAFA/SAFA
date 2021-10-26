<template>
  <v-container>
    <v-stepper v-model="currentStep">
      <v-stepper-header>
        <template v-for="(stepName, stepIndex) in stepNames">
          <v-stepper-step
            :complete="currentStep > stepIndex + 1"
            :step="stepIndex + 1"
            :key="stepName"
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
          <ProjectSelector
            :isOpen="isOpen"
            @onProjectSelected="selectProject"
            @onProjectUnselected="unselectProject"
          />
        </v-stepper-content>

        <v-stepper-content :step="versionStep">
          <VersionSelector
            v-if="selectedProject !== undefined"
            :isOpen="isOpen"
            :project="selectedProject"
            @onVersionSelected="selectVersion"
            @onVersionUnselected="unselectVersion"
          />
        </v-stepper-content>

        <slot name="afterItems" />
      </v-stepper-items>
    </v-stepper>
  </v-container>
</template>

<script lang="ts">
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import ProjectSelector from "@/components/common/modals/ProjectSelector.vue";
import VersionSelector from "@/components/common/modals/VersionSelector.vue";
import Vue, { PropType } from "vue";
import {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
} from "@/types/common-components";

export default Vue.extend({
  name: "ProjectAndVersionModal",
  components: {
    ProjectSelector,
    VersionSelector,
  },
  props: {
    beforeSteps: {
      type: Array as PropType<Array<string>>,
      required: false,
      default: () => [] as string[],
    },
    currentSteps: {
      type: Array as PropType<Array<string>>,
      required: false,
      default: () =>
        ["Select a Project to Modify", "Select a Project Version"] as string[],
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
  },
  methods: {
    selectProject(project: ProjectIdentifier) {
      this.project = project;
    },
    unselectProject() {
      this.project = undefined;
    },
    selectVersion(version: ProjectVersion) {
      this.projectVersion = version;
    },
    unselectVersion() {
      this.projectVersion = undefined;
    },
  },
});
</script>
