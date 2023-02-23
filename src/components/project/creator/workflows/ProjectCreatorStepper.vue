<template>
  <panel-card>
    <stepper
      v-model="currentStep"
      :steps="steps"
      submit-text="Create Project"
      @submit="handleSave()"
    >
      <template #1>
        <project-identifier-input
          v-model:name="name"
          v-model:description="description"
          data-cy-description="input-project-description-standard"
          data-cy-name="input-project-name-standard"
        />
      </template>
      <template #2>
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
      </template>
      <template #3>
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
      </template>
      <template #4>
        <tim-tree
          :artifact-panels="artifactUploader.panels"
          :in-view="currentStep === 4"
          :trace-panels="traceUploader.panels"
        />
      </template>
    </stepper>
  </panel-card>
</template>

<script lang="ts">
export default {
  name: "ProjectCreatorStepper",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { ArtifactMap, StepperStep } from "@/types";
import { projectSaveStore } from "@/hooks";
import {
  createArtifactUploader,
  createTraceUploader,
  handleImportProject,
} from "@/api";
import { Stepper, PanelCard } from "@/components/common";
import { TimTree } from "@/components/graph";
import { ProjectIdentifierInput } from "@/components/project/base";
import { FileUploader, ArtifactTypeCreator, TraceFileCreator } from "../panels";

const steps = ref<StepperStep[]>([
  { title: "Name Project", done: false },
  { title: "Upload Artifacts", done: true },
  { title: "Upload Trace Links", done: true },
  { title: "View TIM", done: true },
]);
const currentRoute = useRoute();
const currentStep = ref(1);
const artifactUploader = ref(createArtifactUploader());
const traceUploader = ref(createTraceUploader());

const name = computed({
  get: () => projectSaveStore.name,
  set: (value) => (projectSaveStore.name = value),
});

const description = computed({
  get: () => projectSaveStore.description,
  set: (value) => (projectSaveStore.description = value),
});

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
  steps.value[stepIndex].done = isValid;
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
function handleSave(): void {
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
  () => projectSaveStore.name,
  (name) => {
    steps.value[0].done = !!name;
  }
);

watch(
  () => currentRoute.path,
  () => handleClearData()
);
</script>
