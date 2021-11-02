<template>
  <GenericStepperModal
    v-model="currentStep"
    title="Create a New Project"
    size="l"
    :steps="steps"
    :isOpen="isOpen"
    :isLoading="isLoading"
    @onClose="onClose"
    @onReset="clearData"
    @onSubmit="$emit('onSubmit')"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <v-container class="pa-10">
          <ProjectCreator
            v-bind:name.sync="name"
            v-bind:description.sync="description"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-container class="pa-10">
          <ArtifactFileUploader
            :artifactFiles="artifactFiles"
            @onChange="artifactFiles = $event"
            @onIsValid="setStepIsValid(1, true)"
            @onIsInvalid="setStepIsValid(1, false)"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-container class="pa-10">
          <TraceFileUploader
            :traceFiles="traceFiles"
            :artifactTypes="artifactTypes"
            :artifactMap="artifactMap"
            @onChange="traceFiles = $event"
            @onIsValid="setStepIsValid(2, true)"
            @onIsInvalid="setStepIsValid(2, false)"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="4">
        <v-container class="pa-10">
          <ProjectConfirmation @onConfirm="saveProject" :project="project" />
        </v-container>
      </v-stepper-content>
    </template>

    <template v-slot:action:main>
      <v-row v-if="currentStep === 4" justify="center">
        <v-btn color="secondary" @click="saveProject()">Create Project</v-btn>
      </v-row>
      <v-row>
        <GenericConfirmDialog
          :isOpen="isConfirmOpen"
          title="Project In Progress"
          body="Closing will delete any progress you have made."
          @onSubmit="onConfirmClose"
          @onClose="isConfirmOpen = false"
        />
      </v-row>
    </template>
  </GenericStepperModal>
</template>

<script lang="ts">
import Vue from "vue";
import GenericStepperModal from "@/components/common/generic/GenericStepperModal.vue";
import type {
  ArtifactFile,
  StepState,
  TraceFile,
} from "@/types/common-components";
import ProjectCreator from "@/components/project/shared/ProjectIdentifierInput.vue";
import ArtifactFileUploader from "@/components/project/creator/artifact-uploader/ArtifactUploader.vue";
import TraceFileUploader from "@/components/project/creator/trace-uploader/TraceUploader.vue";
import { TraceLink } from "@/types/domain/links";
import { Artifact } from "@/types/domain/artifact";
import ProjectConfirmation from "@/components/project/creator/ProjectConfirmation.vue";
import { saveOrUpdateProject } from "@/api/project-api";
import { Project } from "@/types/domain/project";
import { ProjectCreationResponse } from "@/types/api";
import { projectModule } from "@/store";
import GenericConfirmDialog from "@/components/common/generic/GenericConfirmDialog.vue";

export default Vue.extend({
  name: "project-creator-modal",
  components: {
    GenericStepperModal,
    ProjectCreator,
    ArtifactFileUploader,
    TraceFileUploader,
    ProjectConfirmation,
    GenericConfirmDialog,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      steps: [
        ["Name Project", false],
        ["Upload Artifacts", false],
        ["Upload Trace Links", true],
        ["View TIM", false],
      ] as StepState[],
      name: "",
      description: "",
      currentStep: 1,
      isLoading: false,
      artifactFiles: [] as ArtifactFile[],
      traceFiles: [] as TraceFile[],
      isConfirmOpen: false,
    };
  },
  methods: {
    setStepIsValid(stepIndex: number, isValid: boolean): void {
      Vue.set(this.steps, stepIndex, [this.steps[stepIndex][0], isValid]);
    },
    clearData() {
      this.name = "";
      this.description = "";
      this.currentStep = 1;
      this.isLoading = false;
      this.artifactFiles = [];
      this.traceFiles = [];
    },
    onClose() {
      this.isConfirmOpen = true;
    },
    saveProject(): void {
      this.isLoading = true;
      saveOrUpdateProject(this.project)
        .then((projectCreationResponse: ProjectCreationResponse) => {
          projectModule.setProjectCreationResponse(projectCreationResponse);
          this.$emit("onClose");
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    onConfirmClose(): void {
      this.$emit("onClose");
    },
  },
  computed: {
    artifactMap(): Record<string, Artifact> {
      const artifactMap: Record<string, Artifact> = {};
      this.artifacts.forEach((a) => (artifactMap[a.name] = a));
      return artifactMap;
    },
    artifacts(): Artifact[] {
      let artifacts: Artifact[] = [];
      this.artifactFiles.forEach((artifactFile) => {
        if (artifactFile.artifacts !== undefined) {
          artifacts = artifacts.concat(artifactFile.artifacts);
        }
      });
      return artifacts;
    },
    traces(): TraceLink[] {
      let traces: TraceLink[] = [];
      this.traceFiles.forEach((traceFile) => {
        if (traceFile.traces !== undefined) {
          traces = traces.concat(traceFile.traces);
        }
      });
      return traces;
    },
    project(): Project {
      return {
        projectId: "",
        name: this.name,
        description: this.description,
        artifacts: this.artifacts,
        traces: this.traces,
      };
    },
    totalSteps(): number {
      return this.steps.length;
    },
    combinedState(): string {
      return this.name + this.description;
    },
    artifactTypes(): string[] {
      return this.artifactFiles.map((f) => f.type);
    },
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
    currentStep(nextStep: number): void {
      if (nextStep >= 2) {
        Vue.set(this.steps, 0, [this.name, true]);
      }
    },
    name(): void {
      const isFirstStepValid = this.name !== "";
      Vue.set(this.steps, 0, [this.name, isFirstStepValid]);
    },
  },
});
</script>
