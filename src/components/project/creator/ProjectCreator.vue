<template>
  <generic-stepper v-model="currentStep" :steps="steps">
    <v-row>Create a new project</v-row>
    <template v-slot:items>
      <v-stepper-content step="1">
        <v-container>
          <ProjectIdentifierInput
            v-bind:name.sync="name"
            v-bind:description.sync="description"
          />
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-container>
          <generic-uploader
            item-name="artifact"
            :uploader="artifactUploader"
            :artifact-map="artifactMap"
            @onChange="artifactUploader.panels = $event"
            @onIsValid="setStepIsValid(1, true)"
            @onIsInvalid="setStepIsValid(1, false)"
          >
            <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
              <artifact-type-creator-modal
                :is-open="isCreatorOpen"
                :artifact-types="artifactTypes"
                @onSubmit="onAddFile"
                @onClose="onClose"
              />
            </template>
          </generic-uploader>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-container>
          <generic-uploader
            item-name="trace link"
            :uploader="traceUploader"
            :artifact-map="artifactMap"
            :default-valid-state="true"
            @onChange="traceUploader.panels = $event"
            @onIsValid="setStepIsValid(2, true)"
            @onIsInvalid="setStepIsValid(2, false)"
          >
            <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
              <trace-file-creator
                :is-open="isCreatorOpen"
                :trace-files="traceFiles"
                :artifact-types="artifactTypes"
                @onSubmit="onAddFile"
                @onClose="onClose"
              />
            </template>
          </generic-uploader>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="4">
        <v-container class="pa-10">
          <v-row>
            <leave-confirmation-modal
              :project="project"
              @onConfirm="saveProject"
            />
          </v-row>
          <v-row>
            <v-divider />
          </v-row>
          <v-row v-if="currentStep === 4" justify="center" class="mt-5">
            <v-btn color="primary" @click="saveProject()">
              Create Project
            </v-btn>
          </v-row>
        </v-container>
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import {
  Artifact,
  Project,
  ProjectCreationResponse,
  StepState,
  TraceFile,
  TraceLink,
} from "@/types";
import { saveOrUpdateProject } from "@/api";
import { appModule, projectModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import { GenericStepper } from "@/components";
import { ProjectIdentifierInput } from "@/components/project/shared";
import { createTraceUploader, createArtifactUploader } from "./definitions";
import {
  TraceFileCreator,
  ArtifactTypeCreatorModal,
  LeaveConfirmationModal,
} from "./modals";
import { GenericUploader } from "./validation-panels";

const PROJECT_IDENTIFIER_STEP_NAME = "Name Project";

export default Vue.extend({
  components: {
    GenericStepper,
    ProjectIdentifierInput,
    GenericUploader,
    LeaveConfirmationModal,
    ArtifactTypeCreatorModal,
    TraceFileCreator,
  },
  data() {
    return {
      steps: [
        [PROJECT_IDENTIFIER_STEP_NAME, false],
        ["Upload Artifacts", false],
        ["Upload Trace Links", true],
        ["View TIM", false],
      ] as StepState[],
      name: "",
      description: "",
      currentStep: 1,
      isConfirmOpen: false,
      traceUploader: createTraceUploader(),
      artifactUploader: createArtifactUploader(),
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
      this.artifactUploader = createArtifactUploader();
      this.traceUploader = createTraceUploader();
    },

    saveProject(): void {
      appModule.SET_IS_LOADING(true);
      saveOrUpdateProject(this.project)
        .then((projectCreationResponse: ProjectCreationResponse) => {
          projectModule.setProjectCreationResponse(projectCreationResponse);
          navigateTo(Routes.ARTIFACT_TREE);
          this.clearData();
        })
        .finally(() => {
          appModule.SET_IS_LOADING(false);
        });
    },
    onConfirmClose(): void {
      this.isConfirmOpen = false;
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
      this.artifactUploader.panels.forEach(({ projectFile }) => {
        if (projectFile.artifacts !== undefined) {
          artifacts = artifacts.concat(projectFile.artifacts);
        }
      });
      return artifacts;
    },
    artifactTypes(): string[] {
      return this.artifactUploader.panels.map((p) => p.projectFile.type);
    },
    traces(): TraceLink[] {
      let traces: TraceLink[] = [];
      this.traceUploader.panels.forEach(({ projectFile }) => {
        if (projectFile.traces !== undefined) {
          traces = traces.concat(projectFile.traces);
        }
      });
      return traces;
    },
    traceFiles(): TraceFile[] {
      return this.traceUploader.panels.map((p) => p.projectFile);
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
  },
  watch: {
    currentStep(stepNumber: number): void {
      if (stepNumber === 1) {
        const hasName = this.name !== "";
        Vue.set(this.steps, 0, [PROJECT_IDENTIFIER_STEP_NAME, hasName]);
      }
      if (stepNumber === 2) {
        Vue.set(this.steps, 0, [this.name, true]);
      }
    },
    name(): void {
      const hasName = this.name !== "";
      Vue.set(this.steps, 0, [PROJECT_IDENTIFIER_STEP_NAME, hasName]);
    },
  },
});
</script>
