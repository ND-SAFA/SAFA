<template>
  <GenericModal
    :title="title"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @onClose="onClose"
  >
    <template v-slot:body>
      <ProjectAndVersionModal
        v-model="currentStep"
        v-bind:selectedProject.sync="selectedProject"
        v-bind:selectedVersion.sync="selectedVersion"
        :isOpen="isOpen"
        :stepNames="projectVersionStepNames"
        :beforeSteps="beforeStepNames"
        :afterSteps="afterStepNames"
      >
        <template v-slot:beforeItems>
          <slot name="beforeItems" />
        </template>
        <template v-slot:afterItems>
          <slot name="afterItems" />
        </template>
      </ProjectAndVersionModal>
    </template>
    <template v-slot:actions>
      <v-container class="ma-0 pa-0">
        <v-row class="ma-0">
          <v-col cols="4" align-self="center">
            <v-btn v-if="currentStep > 1" @click="onStepBack" fab small>
              <v-icon id="upload-button">mdi-arrow-left</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="4">
            <slot name="action:main" />
          </v-col>
          <v-col cols="4" align-self="center">
            <v-row justify="end">
              <v-btn
                v-if="isStepDone"
                @click="onStepForward"
                fab
                small
                :color="currentStep === numberOfSteps ? 'secondary' : undefined"
              >
                <v-icon id="upload-button">{{
                  currentStep === numberOfSteps
                    ? "mdi-check"
                    : "mdi-arrow-right"
                }}</v-icon>
              </v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ProjectAndVersionModal from "@/components/common/modals/ProjectAndVersionModal.vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";
import {
  OptionalProjectIdentifier,
  OptionalProjectVersion,
} from "@/types/common-components";

export default Vue.extend({
  name: "baseline-version-modal",
  components: {
    ProjectAndVersionModal,
    GenericModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    projectVersionStepNames: {
      type: Array as PropType<Array<string>>,
      required: true,
    },
    beforeSteps: {
      type: Array as PropType<Array<[string, boolean]>>,
      required: false,
      default: () => [] as [string, boolean][],
    },
    afterSteps: {
      type: Array as PropType<Array<[string, boolean]>>,
      required: false,
      default: () => [] as [string, boolean][],
    },
    project: {
      type: Object as PropType<OptionalProjectIdentifier>,
      required: false,
    },
    version: {
      type: Object as PropType<OptionalProjectVersion>,
      required: false,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    value: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      currentStep: this.value,
      fileSelectorOpen: false,
    };
  },
  methods: {
    clearData() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.$emit("update:isLoading", false);
      this.fileSelectorOpen = false;
      this.currentStep = 1;
    },
    onClose() {
      this.selectedProject = undefined;
      this.selectedVersion = undefined;
      this.$emit("onClose");
    },

    onStepBack(): void {
      this.currentStep--;
    },
    onStepForward(): void {
      if (this.currentStep === this.numberOfSteps) {
        this.$emit("onSubmit");
      } else {
        this.currentStep++;
      }
    },
  },
  computed: {
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
    numberOfSteps(): number {
      return (
        this.beforeSteps.length +
        this.projectVersionStepNames.length +
        this.afterSteps.length
      );
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
    currentStep(newStep: number): void {
      this.$emit("input", newStep);
    },
  },
});
</script>
