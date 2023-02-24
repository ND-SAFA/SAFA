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
        <artifact-type-step />
      </template>
      <template #3>
        <trace-matrix-step />
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
import { projectSaveStore } from "@/hooks";
import { handleImportProject } from "@/api";
import { Stepper, PanelCard } from "@/components/common";
import { TimTree } from "@/components/graph";
import { ProjectIdentifierInput } from "@/components/project/base";
import {
  ArtifactTypeStep,
  TraceMatrixStep,
} from "@/components/project/creator/steps";

const steps = ref<StepperStep[]>([
  { title: "Name Project", done: false },
  { title: "Upload Artifacts", done: true },
  { title: "Upload Trace Links", done: true },
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
 * Attempts to create a project.
 */
function handleSave(): void {
  handleImportProject(projectSaveStore.creationRequest, {
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
