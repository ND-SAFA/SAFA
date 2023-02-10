<template>
  <stepper
    v-model="currentStep"
    :steps="steps"
    submit-text="Create Project"
    @submit="saveProject()"
  >
    <template #items>
      <v-stepper-content step="1">
        <project-identifier-input
          v-model:description="projectSaveStore.description"
          v-model:name="projectSaveStore.name"
          data-cy-description="input-project-description-standard"
          data-cy-name="input-project-name-standard"
        />
      </v-stepper-content>

      <v-stepper-content step="2">
        <file-uploader
          :artifact-map="artifactMap"
          :uploader="artifactUploader"
          item-name="artifact"
          @change="artifactUploader.panels = $event"
          @upload:valid="setStepIsValid(1, true)"
          @upload:invalid="setStepIsValid(1, false)"
        >
          <template #creator="{ isCreatorOpen, onAddFile, onClose }">
            <artifact-type-creator
              :artifact-types="artifactTypes"
              :is-open="isCreatorOpen"
              @close="onClose"
              @submit="onAddFile"
            />
          </template>
        </file-uploader>
      </v-stepper-content>

      <v-stepper-content step="3">
        <file-uploader
          :artifact-map="artifactMap"
          :default-valid-state="true"
          :uploader="traceUploader"
          item-name="trace matrix"
          @change="traceUploader.panels = $event"
          @upload:valid="setStepIsValid(2, true)"
          @upload:invalid="setStepIsValid(2, false)"
        >
          <template #creator="{ isCreatorOpen, onAddFile, onClose }">
            <trace-file-creator
              :artifact-types="artifactTypes"
              :is-open="isCreatorOpen"
              :trace-files="traceFiles"
              @close="onClose"
              @submit="onAddFile"
            />
          </template>
        </file-uploader>
      </v-stepper-content>

      <v-stepper-content step="4">
        <tim-tree
          :artifact-panels="artifactUploader.panels"
          :in-view="currentStep === 4"
          :trace-panels="traceUploader.panels"
        />
      </v-stepper-content>
    </template>
  </stepper>
</template>

<script lang="ts">
export default {
  name: "ProjectCreatorStepper",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { ArtifactMap, StepState } from "@/types";
import { projectSaveStore } from "@/hooks";
import {
  createArtifactUploader,
  createTraceUploader,
  handleImportProject,
} from "@/api";
import { Stepper } from "@/components/common";
import { TimTree } from "@/components/graph";
import { ProjectIdentifierInput } from "@/components/project/base";
import { FileUploader, ArtifactTypeCreator, TraceFileCreator } from "../panels";

const PROJECT_IDENTIFIER_STEP_NAME = "Name Project";

const steps = ref<StepState[]>([
  [PROJECT_IDENTIFIER_STEP_NAME, false],
  ["Upload Artifacts", true],
  ["Upload Trace Links", true],
  ["View TIM", true],
]);
const currentRoute = useRoute();
const currentStep = ref(1);
const artifactUploader = ref(createArtifactUploader());
const traceUploader = ref(createTraceUploader());

const artifactMap = computed<ArtifactMap>(() =>
  artifactUploader.value.panels
    .map(({ projectFile }) => projectFile.artifacts || [])
    .reduce((acc, cur) => [...acc, ...cur], [])
    .map((artifact) => ({ [artifact.name]: artifact }))
    .reduce((acc, cur) => ({ ...acc, ...cur }), {})
);

const artifactTypes = computed(() =>
  artifactUploader.value.panels.map((p) => p.projectFile.type)
);

const traceFiles = computed(() =>
  traceUploader.value.panels.map((p) => p.projectFile)
);

/**
 * Sets the valid state of a step.
 * @param stepIndex - The step cto change.
 * @param isValid - Whether the step is valid.
 */
function setStepIsValid(stepIndex: number, isValid: boolean): void {
  steps.value[stepIndex] = [steps.value[stepIndex][0], isValid];
}

/**
 * Clears stepper data.
 */
function handleClearData() {
  projectSaveStore.resetProject();
  currentStep.value = 1;
  artifactUploader.value = createArtifactUploader();
  traceUploader.value = createTraceUploader();
}

/**
 * Attempts to create a project.
 */
function saveProject(): void {
  handleImportProject(
    projectSaveStore.getCreationRequest(
      artifactUploader.value,
      traceUploader.value
    ),
    {
      onSuccess: () => handleClearData(),
    }
  );
}

watch(
  () => currentStep.value,
  (stepNumber) => {
    if (stepNumber === 1) {
      const hasName = projectSaveStore.name !== "";

      steps.value[0] = [PROJECT_IDENTIFIER_STEP_NAME, hasName];
    } else if (stepNumber === 2) {
      steps.value[0] = [projectSaveStore.name, true];
    }
  }
);

watch(
  () => projectSaveStore.name,
  (newName) => {
    steps.value[0] = [PROJECT_IDENTIFIER_STEP_NAME, newName !== ""];
  }
);

watch(
  () => currentRoute.path,
  () => handleClearData()
);
</script>
