<template>
  <panel-card :color="panelColor">
    <stepper
      v-model="currentStep"
      :steps="steps"
      :minimal="props.minimal"
      data-cy="project-version-stepper"
      @submit="handleSubmit"
    >
      <template #1>
        <project-selector-table
          :minimal="props.minimal"
          :open="isProjectStep"
          @selected="handleProjectSelect"
        />
      </template>
      <template #2>
        <version-selector-table
          :minimal="props.minimal"
          :open="isVersionStep"
          :project="selectedProject"
          @selected="handleVersionSelect"
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
import ProjectSelectorTable from "./ProjectSelectorTable.vue";
import VersionSelectorTable from "./VersionSelectorTable.vue";

const props = defineProps<{
  /**
   * Whether to display minimal information.
   */
  minimal?: boolean;
}>();

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
const panelColor = computed(() => (props.minimal ? "transparent" : "primary"));

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
async function handleSubmit(): Promise<void> {
  if (!selectedProject.value || !selectedVersion.value) return;

  loading.value = true;

  await handleLoadVersion(selectedVersion.value.versionId);

  loading.value = false;
  handleClear();
}
</script>
