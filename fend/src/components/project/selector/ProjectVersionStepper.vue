<template>
  <panel-card :color="panelColor">
    <stepper
      v-if="!permissionStore.isDemo || !getVersionApiStore.loadLoading"
      v-model="currentStep"
      :steps="steps"
      :minimal="props.minimal"
      :loading="getVersionApiStore.loadLoading"
      data-cy="project-version-stepper"
      @submit="handleSubmit"
    >
      <template #1>
        <project-selector-table
          :minimal="props.minimal"
          :open="isProjectStep"
          :team-only="props.teamOnly"
          @selected="handleProjectSelect"
        />
      </template>
      <template #2>
        <version-selector-table
          v-if="selectedProject"
          :minimal="props.minimal"
          :disabled="getVersionApiStore.loadLoading"
          :open="isVersionStep"
          :project="selectedProject"
          @selected="handleVersionSelect"
        />
      </template>
    </stepper>
    <flex-box v-else align="center" justify="center" full-width t="2">
      <q-circular-progress
        rounded
        indeterminate
        size="60px"
        :thickness="0.2"
        color="primary"
      />
    </flex-box>
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
import {
  StepperStep,
  IdentifierSchema,
  VersionSchema,
  MinimalProps,
} from "@/types";
import { versionToString } from "@/util";
import { getVersionApiStore, permissionStore, projectStore } from "@/hooks";
import { Stepper, PanelCard } from "@/components/common";
import FlexBox from "@/components/common/display/content/FlexBox.vue";
import { ProjectSelectorTable, VersionSelectorTable } from "./table";

const props = defineProps<MinimalProps & { teamOnly?: boolean }>();

const defaultProjectStep = (): StepperStep => ({
  title: "Select a Project",
  done: false,
});
const defaultVersionStep = (): StepperStep => ({
  title: "Select a Version",
  done: false,
});

const currentStep = ref(1);
const steps = ref([defaultProjectStep(), defaultVersionStep()]);
const selectedProject = ref<IdentifierSchema>();
const selectedVersion = ref<VersionSchema>();

const isProjectStep = computed(() => currentStep.value === 1);
const isVersionStep = computed(() => currentStep.value === 2);
const panelColor = computed(() => (props.minimal ? "transparent" : undefined));

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
 * @param project - The project to select, or an empty selection.
 */
function handleProjectSelect(project: IdentifierSchema | undefined) {
  selectedProject.value = project;

  if (project) {
    currentStep.value++;
    steps.value[0] = {
      title: project.name,
      done: true,
    };
  } else {
    steps.value = [defaultProjectStep(), defaultVersionStep()];
  }

  handleVersionSelect(undefined);
}

/**
 * Selects a version.
 * @param version - The version to select, or an empty selection.
 */
function handleVersionSelect(version: VersionSchema | undefined) {
  selectedVersion.value = version;

  if (version) {
    steps.value[1] = {
      title: versionToString(version),
      done: true,
    };

    handleSubmit();
  } else {
    steps.value[1] = defaultVersionStep();
  }
}

/**
 * Loads the selected project.
 */
function handleSubmit(): void {
  if (
    !selectedProject.value ||
    !selectedVersion.value ||
    getVersionApiStore.loadLoading
  )
    return;

  getVersionApiStore
    .handleLoad(selectedVersion.value.versionId)
    .then(() => handleClear());
}
</script>
