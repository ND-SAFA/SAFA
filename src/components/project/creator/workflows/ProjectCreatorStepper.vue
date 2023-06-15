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
        <file-panel-list
          label="Artifact Type"
          variant="artifact"
          @validate="handleValidateArtifacts"
        />
      </template>
      <template #3>
        <file-panel-list
          label="Trace Matrix"
          variant="trace"
          @validate="handleValidateTraces"
        />
      </template>
      <template #4>
        <tim-tree :visible="currentStep === 4" />
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
import { StepperStep } from "@/types";
import { createProjectApiStore, projectSaveStore } from "@/hooks";
import { Stepper, PanelCard } from "@/components/common";
import { TimTree } from "@/components/graph";
import { ProjectIdentifierInput } from "@/components/project/base";
import { FilePanelList } from "@/components/project/creator/steps";

const steps = ref<StepperStep[]>([
  { title: "Name Project", done: false },
  { title: "Upload Artifacts", done: false },
  { title: "Upload Trace Links", done: false },
  { title: "View TIM", done: true },
]);
const currentRoute = useRoute();
const currentStep = ref(1);

const name = computed({
  get: () => projectSaveStore.name,
  set: (value) => (projectSaveStore.name = value),
});

const description = computed({
  get: () => projectSaveStore.description,
  set: (value) => (projectSaveStore.description = value),
});

/**
 * Clears stepper data.
 */
function handleClearData() {
  projectSaveStore.resetProject();
  currentStep.value = 1;
}

/**
 * Updates whether the artifact step is valid.
 * @param isValid - Whether the step is valid.
 */
function handleValidateArtifacts(isValid: boolean): void {
  steps.value[1].done = isValid;
}

/**
 * Updates whether the trace step is valid.
 * @param isValid - Whether the step is valid.
 */
function handleValidateTraces(isValid: boolean): void {
  steps.value[2].done = isValid;
}

/**
 * Attempts to create a project.
 */
function handleSave(): void {
  createProjectApiStore.handleImportProject({
    onSuccess: () => handleClearData(),
  });
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
