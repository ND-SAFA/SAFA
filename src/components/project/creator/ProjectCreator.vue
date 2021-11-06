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
          <GenericUploader
            :uploader="artifactUploader"
            :artifactMap="artifactMap"
            noItemError="No artifact types have been defined."
            @onChange="artifactUploader.panels = $event"
            @onIsValid="setStepIsValid(1, true)"
            @onIsInvalid="setStepIsValid(1, false)"
          >
            <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
              <ArtifactTypeCreatorModal
                :isOpen="isCreatorOpen"
                :artifactTypes="artifactTypes"
                @onSubmit="onAddFile"
                @onClose="onClose"
              />
            </template>
          </GenericUploader>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-container class="pa-10">
          <GenericUploader
            :uploader="traceUploader"
            :artifactMap="artifactMap"
            :defaultValidState="true"
            noItemError="No trace links have been defined."
            @onChange="traceUploader.panels = $event"
            @onIsValid="setStepIsValid(2, true)"
            @onIsInvalid="setStepIsValid(2, false)"
          >
            <template v-slot:creator="{ isCreatorOpen, onAddFile, onClose }">
              <TraceFileCreator
                :isOpen="isCreatorOpen"
                :traceFiles="traceFiles"
                :artifactTypes="artifactTypes"
                @onSubmit="onAddFile"
                @onClose="onClose"
              />
            </template>
          </GenericUploader>
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
          body="Closing panel will delete any progress you have made."
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
import {
  StepState,
  TraceFile,
  ProjectCreationResponse,
  TraceLink,
  Artifact,
  Project,
} from "@/types";
import ProjectCreator from "@/components/project/shared/ProjectIdentifierInput.vue";
import ProjectConfirmation from "@/components/project/creator/modals/LeaveConfirmationModal.vue";
import { saveOrUpdateProject } from "@/api";
import { projectModule } from "@/store";
import GenericConfirmDialog from "@/components/common/generic/GenericConfirmDialog.vue";
import GenericUploader from "@/components/project/creator/validation-panels/GenericUploader.vue";
import ArtifactTypeCreatorModal from "@/components/project/creator/modals/ArtifactTypeCreatorModal.vue";
import { createArtifactUploader } from "@/components/project/creator/definitions/artifact-uploader";
import TraceFileCreator from "@/components/project/creator/modals/TraceFileCreator.vue";
import { createTraceUploader } from "@/components/project/creator/definitions/trace-uploader";

export default Vue.extend({
  name: "project-creator-modal",
  components: {
    GenericStepperModal,
    ProjectCreator,
    GenericUploader,
    ProjectConfirmation,
    GenericConfirmDialog,
    ArtifactTypeCreatorModal,
    TraceFileCreator,
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
      this.isLoading = false;
      this.artifactUploader = createArtifactUploader();
      this.traceUploader = createTraceUploader();
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
