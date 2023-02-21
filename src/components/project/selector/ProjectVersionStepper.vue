<template>
  <panel-card>
    <stepper
      v-model="currentStep"
      :steps="steps"
      data-cy="project-version-stepper"
      @submit="handleSubmit"
    >
      <template #1>
        <project-selector
          :is-open="isProjectStep"
          @selected="selectProject"
          @unselected="unselectProject"
        />
      </template>
      <template #2>
        <version-selector
          :is-open="isVersionStep"
          :project="selectedProject"
          @selected="selectVersion"
          @unselected="unselectVersion"
        />
      </template>
    </stepper>
  </panel-card>
</template>

<script lang="ts">
/**
 * Presents a stepper in a modal for selecting a project and version.
 */
export default {
  name: "ProjectVersionStepper",
};
</script>

<script setup lang="ts">
import { ref, computed } from "vue";
import { StepperStep, IdentifierSchema, VersionSchema } from "@/types";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { handleLoadVersion } from "@/api";
import { Stepper, PanelCard } from "@/components/common";
import ProjectSelector from "./ProjectSelector.vue";
import VersionSelector from "./VersionSelector.vue";

const defaultProjectStep = (): StepperStep => ({
  title: "Select a Project",
  done: false,
});
const defaultVersionStep = (): StepperStep => ({
  title: "Select a Version",
  done: false,
});

const loading = ref(false);
const currentStep = ref(1);
const steps = ref([defaultProjectStep(), defaultVersionStep()]);
const selectedProject = ref<IdentifierSchema | undefined>(undefined);
const selectedVersion = ref<VersionSchema | undefined>(undefined);

const isProjectStep = computed(() => currentStep.value === 1);
const isVersionStep = computed(() => currentStep.value === 2);

/**
 * Clears all modal data.
 */
function handleClear() {
  const isProjectDefined = projectStore.isProjectDefined;

  selectedProject.value = isProjectDefined ? projectStore.project : undefined;
  selectedVersion.value = undefined;
  currentStep.value = 1;

  steps.value = [
    isProjectDefined
      ? {
          title: projectStore.project.name,
          done: true,
        }
      : defaultProjectStep(),
    defaultVersionStep(),
  ];
}

/**
 * Selects a project.
 * @param project - The project to select.
 * @param goToNextStep - If true, the step will be incremented.
 */
function selectProject(project: IdentifierSchema, goToNextStep = false) {
  selectedProject.value = project;
  unselectVersion();

  steps.value[0] = {
    title: project.name,
    done: true,
  };

  if (goToNextStep) currentStep.value++;
}

/**
 * Deselects a project.
 */
function unselectProject() {
  selectedProject.value = undefined;
  steps.value = [defaultProjectStep(), defaultVersionStep()];
}

/**
 * Selects a version.
 * @param version - The version to select.
 */
function selectVersion(version: VersionSchema) {
  selectedVersion.value = version;

  steps.value[1] = {
    title: versionToString(version),
    done: true,
  };

  handleSubmit();
}

/**
 * Deselects a version.
 */
function unselectVersion() {
  selectedVersion.value = undefined;
  steps.value[1] = defaultVersionStep();
}

/**
 * Loads the selected project.
 */
async function handleSubmit(): Promise<void> {
  if (!selectedProject.value || !selectedVersion.value) return;

  loading.value = true;

  await handleLoadVersion(selectedVersion.value.versionId);

  loading.value = false;
  handleClear();
}
</script>
