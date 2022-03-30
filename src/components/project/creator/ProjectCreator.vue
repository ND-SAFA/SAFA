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
        <project-initialization
          v-bind:name.sync="name"
          v-bind:description.sync="description"
        />
      </v-stepper-content>

      <v-stepper-content step="2">
        <generic-uploader
          item-name="artifact"
          :uploader="artifactUploader"
          :artifact-map="artifactMap"
          @change="artifactUploader.panels = $event"
          @upload:valid="setStepIsValid(1, true)"
          @upload:invalid="setStepIsValid(1, false)"
        >
          <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
            <artifact-type-creator
              :is-open="isCreatorOpen"
              :artifact-types="artifactTypes"
              @submit="onAddFile"
              @close="onClose"
            />
          </template>
        </generic-uploader>
      </v-stepper-content>

      <v-stepper-content step="3">
        <generic-uploader
          item-name="trace link"
          :uploader="traceUploader"
          :artifact-map="artifactMap"
          :default-valid-state="true"
          @change="traceUploader.panels = $event"
          @upload:valid="setStepIsValid(2, true)"
          @upload:invalid="setStepIsValid(2, false)"
        >
          <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
            <trace-file-creator
              :is-open="isCreatorOpen"
              :trace-files="traceFiles"
              :artifact-types="artifactTypes"
              @submit="onAddFile"
              @close="onClose"
            />
          </template>
        </generic-uploader>
      </v-stepper-content>

      <v-stepper-content step="4">
        <tim-tree
          :artifact-panels="artifactUploader.panels"
          :trace-panels="traceUploader.panels"
          :in-view="currentStep === 4"
        />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import {
  Artifact,
  Project,
  ProjectMembership,
  ProjectRole,
  StepState,
  TraceFile,
  TraceLink,
} from "@/types";
import { createProject } from "@/util";
import { saveOrUpdateProject, setCreatedProject } from "@/api";
import { appModule, sessionModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import { GenericStepper } from "@/components/common";
import { TimTree } from "./tim-tree-view";
import { GenericUploader } from "./validation-panels";
import { createArtifactUploader, createTraceUploader } from "./uploaders";
import {
  ArtifactTypeCreator,
  TraceFileCreator,
  ProjectInitialization,
} from "./panels";

const PROJECT_IDENTIFIER_STEP_NAME = "Name Project";

export default Vue.extend({
  components: {
    ProjectInitialization,
    GenericStepper,
    GenericUploader,
    ArtifactTypeCreator,
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
    saveProject: function (): void {
      appModule.onLoadStart();
      saveOrUpdateProject(this.project)
        .then(async (res) => {
          this.clearData();
          await navigateTo(Routes.ARTIFACT);
          await setCreatedProject(res);
        })
        .finally(() => {
          appModule.onLoadEnd();
        });
    },
  },
  computed: {
    artifactMap(): Record<string, Artifact> {
      return this.artifacts
        .map((artifact) => ({ [artifact.name]: artifact }))
        .reduce((acc, cur) => ({ ...acc, ...cur }), {});
    },
    artifacts(): Artifact[] {
      return this.artifactUploader.panels
        .map(({ projectFile }) => projectFile.artifacts || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
    artifactTypes(): string[] {
      return this.artifactUploader.panels.map((p) => p.projectFile.type);
    },

    traces(): TraceLink[] {
      return this.traceUploader.panels
        .map(({ projectFile }) => projectFile.traces || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
    traceFiles(): TraceFile[] {
      return this.traceUploader.panels.map((p) => p.projectFile);
    },

    project(): Project {
      const user: ProjectMembership = {
        projectMembershipId: "",
        email: sessionModule.userEmail,
        role: ProjectRole.OWNER,
      };

      return createProject({
        name: this.name,
        description: this.description,
        owner: user.email,
        members: [user],
        artifacts: this.artifacts,
        traces: this.traces,
      });
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
    name(newName: string): void {
      Vue.set(this.steps, 0, [PROJECT_IDENTIFIER_STEP_NAME, newName !== ""]);
    },
  },
});
</script>
