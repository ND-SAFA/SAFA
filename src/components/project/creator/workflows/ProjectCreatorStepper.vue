<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="saveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <project-identifier-input
          data-cy-description="input-project-description-standard"
          data-cy-name="input-project-name-standard"
          v-bind:description.sync="description"
          v-bind:name.sync="name"
        />
      </v-stepper-content>

      <v-stepper-content step="2">
        <generic-uploader
          :artifact-map="artifactMap"
          :uploader="artifactUploader"
          item-name="artifact"
          @change="artifactUploader.panels = $event"
          @upload:valid="setStepIsValid(1, true)"
          @upload:invalid="setStepIsValid(1, false)"
        >
          <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
            <artifact-type-creator
              :artifact-types="artifactTypes"
              :is-open="isCreatorOpen"
              @close="onClose"
              @submit="onAddFile"
            />
          </template>
        </generic-uploader>
      </v-stepper-content>

      <v-stepper-content step="3">
        <generic-uploader
          :artifact-map="artifactMap"
          :default-valid-state="true"
          :uploader="traceUploader"
          item-name="trace matrix"
          @change="traceUploader.panels = $event"
          @upload:valid="setStepIsValid(2, true)"
          @upload:invalid="setStepIsValid(2, false)"
        >
          <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
            <trace-file-creator
              :artifact-types="artifactTypes"
              :is-open="isCreatorOpen"
              :trace-files="traceFiles"
              @close="onClose"
              @submit="onAddFile"
            />
          </template>
        </generic-uploader>
      </v-stepper-content>

      <v-stepper-content step="4">
        <tim-tree
          :artifact-panels="artifactUploader.panels"
          :in-view="currentStep === 4"
          :trace-panels="traceUploader.panels"
        />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ArtifactMap,
  ArtifactModel,
  GeneratedMatrixModel,
  MembershipModel,
  ProjectModel,
  ProjectRole,
  StepState,
  TraceFile,
  TraceLinkModel,
} from "@/types";
import { createProject } from "@/util";
import { sessionStore } from "@/hooks";
import {
  createArtifactUploader,
  createTraceUploader,
  handleImportProject,
} from "@/api";
import { GenericStepper } from "@/components/common";
import { ProjectIdentifierInput } from "@/components/project/shared";
import { ArtifactTypeCreator, TraceFileCreator } from "../panels";
import { GenericUploader } from "../validation-panels";
import { TimTree } from "../tim-tree-view";

const PROJECT_IDENTIFIER_STEP_NAME = "Name Project";

export default Vue.extend({
  name: "ProjectCreatorStepper",
  components: {
    ProjectIdentifierInput,
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
        ["Upload Artifacts", true],
        ["Upload Trace Links", true],
        ["View TIM", true],
      ] as StepState[],
      currentStep: 1,

      name: "",
      description: "",

      artifactUploader: createArtifactUploader(),
      traceUploader: createTraceUploader(),
    };
  },
  methods: {
    /**
     * Sets the valid state of a step.
     * @param stepIndex - The step cto change.
     * @param isValid - Whether the step is valid.
     */
    setStepIsValid(stepIndex: number, isValid: boolean): void {
      Vue.set(this.steps, stepIndex, [this.steps[stepIndex][0], isValid]);
    },
    /**
     * Clears stepper data.
     */
    clearData() {
      this.name = "";
      this.description = "";
      this.currentStep = 1;
      this.artifactUploader = createArtifactUploader();
      this.traceUploader = createTraceUploader();
    },
    /**
     * Attempts to create a project.
     */
    saveProject(): void {
      handleImportProject(
        {
          project: this.project,
          requests: this.generatedTraces,
        },
        {
          onSuccess: () => this.clearData(),
        }
      );
    },
  },
  computed: {
    /**
     * @return All artifacts.
     */
    artifacts(): ArtifactModel[] {
      return this.artifactUploader.panels
        .map(({ projectFile }) => projectFile.artifacts || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
    /**
     * @return A collection of all artifacts.
     */
    artifactMap(): ArtifactMap {
      return this.artifacts
        .map((artifact) => ({ [artifact.name]: artifact }))
        .reduce((acc, cur) => ({ ...acc, ...cur }), {});
    },
    /**
     * @return All artifacts types.
     */
    artifactTypes(): string[] {
      return this.artifactUploader.panels.map((p) => p.projectFile.type);
    },
    /**
     * @return All trace links.
     */
    traces(): TraceLinkModel[] {
      return this.traceUploader.panels
        .map(({ projectFile }) => projectFile.traces || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
    /**
     * @return All trace files.
     */
    traceFiles(): TraceFile[] {
      return this.traceUploader.panels.map((p) => p.projectFile);
    },
    /**
     * @return All trace files.
     */
    generatedTraces(): GeneratedMatrixModel[] {
      return this.traceUploader.panels
        .filter(({ projectFile }) => projectFile.isGenerated)
        .map(({ projectFile }) => ({
          source: projectFile.sourceId,
          target: projectFile.targetId,
          method: projectFile.method,
        }));
    },
    /**
     * @return The project to create.
     */
    project(): ProjectModel {
      const user: MembershipModel = {
        projectMembershipId: "",
        email: sessionStore.userEmail,
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
    /**
     * When the step changes, update the project step to include the project's name.
     */
    currentStep(stepNumber: number): void {
      if (stepNumber === 1) {
        const hasName = this.name !== "";
        Vue.set(this.steps, 0, [PROJECT_IDENTIFIER_STEP_NAME, hasName]);
      } else if (stepNumber === 2) {
        Vue.set(this.steps, 0, [this.name, true]);
      }
    },
    /**
     * When the name changes, update the project step to the new name.
     */
    name(newName: string): void {
      Vue.set(this.steps, 0, [PROJECT_IDENTIFIER_STEP_NAME, newName !== ""]);
    },
  },
});
</script>
