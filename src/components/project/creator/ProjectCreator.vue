<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="saveProject()"
  >
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
        <v-container>
          <v-row justify="center">
            <v-col>
              <h1 class="text-h6">Project TIM</h1>
            </v-col>
          </v-row>
          <TimTree
            :artifact-panels="artifactUploader.panels"
            :trace-panels="traceUploader.panels"
            :in-view="currentStep === 4"
          />
        </v-container>
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact, Project, StepState, TraceFile, TraceLink } from "@/types";
import { saveOrUpdateProject } from "@/api";
import { appModule, projectModule } from "@/store";
import { GenericStepper } from "@/components/common";
import { ProjectIdentifierInput } from "@/components/project/shared";
import { createTraceUploader, createArtifactUploader } from "./uploaders";
import { TraceFileCreator, ArtifactTypeCreatorModal } from "./modals";
import { TimTree } from "./tim-tree-view";
import { GenericUploader } from "./validation-panels";
import { navigateTo, Routes } from "@/router";

const PROJECT_IDENTIFIER_STEP_NAME = "Name Project";

export default Vue.extend({
  components: {
    GenericStepper,
    ProjectIdentifierInput,
    GenericUploader,
    ArtifactTypeCreatorModal,
    TraceFileCreator,
    TimTree,
  },
  data() {
    return {
      steps: [
        [PROJECT_IDENTIFIER_STEP_NAME, false],
        ["Upload Artifacts", false],
        ["Upload Trace Links", true],
        ["View TIM", true],
      ] as StepState[],
      name: "",
      description: "",
      currentStep: 1,
      isConfirmOpen: false,
      artifactUploader: createArtifactUploader(),
      traceUploader: createTraceUploader(),
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
        .then(async (res) => {
          await navigateTo(Routes.ARTIFACT_TREE);
          await projectModule.setProjectCreationResponse(res);
        })
        .then(() => this.clearData())
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
