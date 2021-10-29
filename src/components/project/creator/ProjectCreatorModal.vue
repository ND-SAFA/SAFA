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
            @onChange="artifactFiles = $event"
            @onIsValid="setStepIsValid(1, true)"
            @onIsInvalid="setStepIsValid(1, false)"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-container class="pa-10">
          <TraceFileUploader
            :artifactTypes="artifactTypes"
            @change="traceFiles = $event"
            @onIsValid="setStepIsValid(2, true)"
            @onIsInvalid="setStepIsValid(2, false)"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="4">
        <v-container class="pa-10">
          <ProjectConfirmation
            @onConfirm="saveProject"
            :project="{
              name: 'SAFA',
              description: 'Safety Artifact Forest Analysis',
              artifacts: [],
              traces: [],
            }"
          />
        </v-container>
      </v-stepper-content>
    </template>

    <template v-slot:action:main>
      <v-row v-if="currentStep === 4" justify="center">
        <v-btn color="secondary" @click="saveProject()">Create Project</v-btn>
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

export default Vue.extend({
  name: "project-creator-modal",
  components: {
    GenericStepperModal,
    ProjectCreator,
    ArtifactFileUploader,
    TraceFileUploader,
    ProjectConfirmation,
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
        ["Upload Trace Links", false],
        ["View TIM", false],
      ] as StepState[],
      name: "",
      description: "",
      currentStep: 1,
      isLoading: false,
      artifactFiles: [] as ArtifactFile[],
      traceFiles: [] as TraceFile[],
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
    },
    onClose() {
      this.$emit("onClose");
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
  },
  computed: {
    project(): Project {
      let artifacts: Artifact[] = [];
      let traces: TraceLink[] = [];
      this.artifactFiles.forEach((artifactFile) => {
        if (artifactFile.artifacts !== undefined) {
          artifacts = artifacts.concat(artifactFile.artifacts);
        }
      });
      this.traceFiles.forEach((traceFile) => {
        if (traceFile.traces !== undefined) {
          traces = traces.concat(traceFile.traces);
        }
      });
      return {
        projectId: "",
        name: this.name,
        description: this.description,
        artifacts: artifacts,
        traces: traces,
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
      switch (nextStep) {
        case 2:
          Vue.set(this.steps, 0, [this.name, true]);
          break;
        default:
          break;
      }
    },
    name(): void {
      const isFirstStepValid = this.name !== "";
      Vue.set(this.steps, 0, [this.name, isFirstStepValid]);
    },
  },
});
</script>
