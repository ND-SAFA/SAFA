<template>
  <typography
    el="div"
    value="
      During the import process,
      a summary of each individual code file will be generated
      along with an overall summary of the project.
      You will receive an email when the import completes.
    "
  />
  <typography
    el="div"
    secondary
    value="This process may take up to 30 minutes depending on the size of your project."
  />

  <flex-box v-if="status === 'initial'" column align="center" t="4">
    <typography el="div" value="Importing from GitHub:" />
    <attribute-chip
      :value="integrationsStore.gitHubFullProjectName"
      icon="project-add"
      color="primary"
    />
    <typography el="div" value="Generating Data:" class="q-mt-md" />
    <attribute-chip
      value="Project Summary"
      icon="create-artifact"
      color="primary"
    />
    <attribute-chip
      value="File Summaries"
      icon="create-artifact"
      color="primary"
    />
    <flex-box t="4">
      <text-button
        text
        color="gradient"
        class="bd-gradient"
        icon="generate-artifacts"
        :disabled="onboardingStore.error"
        @click="handleGenerate"
      >
        Import & Summarize
      </text-button>
    </flex-box>
  </flex-box>

  <job-loading-sub-step v-if="status === 'loading'" />

  <div v-if="status === 'success'" />

  <q-banner v-if="status === 'error'" rounded class="bg-background q-mt-md">
    <template #avatar>
      <icon variant="error" color="secondary" size="md" class="q-mr-sm" />
    </template>
    <typography
      value="
          On no! It looks like there was an issue with importing from GitHub.
          You can schedule a call with us below to ensure your data gets uploaded properly.
        "
    />
    <template #action>
      <text-button
        text
        color="secondary"
        icon="calendar"
        @click="onboardingStore.handleScheduleCall"
      >
        Schedule a Call
      </text-button>
    </template>
  </q-banner>
</template>

<script lang="ts">
/**
 * The onboarding step to import from GitHub, wait for the import, and display the generated summaries afterward.
 */
export default {
  name: "SummarizeStep",
};
</script>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { integrationsStore, onboardingStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  Icon,
  TextButton,
  Typography,
} from "@/components/common";
import JobLoadingSubStep from "./JobLoadingSubStep.vue";

const status = ref<"initial" | "loading" | "success" | "error">("initial");

/**
 * Sets the status to loading and starts a generation job when the user clicks the import button.
 */
function handleGenerate() {
  status.value = "loading";
  onboardingStore.handleImportProject();
}

/**
 * Updates the status when the job changes.
 */
function updateStatus(moveNext?: boolean) {
  if (onboardingStore.uploadedJob?.status === "IN_PROGRESS") {
    status.value = "loading";
  }
  if (onboardingStore.uploadedJob?.status === "FAILED") {
    status.value = "error";
  } else if (onboardingStore.uploadedJob?.status === "COMPLETED") {
    status.value = "success";

    if (!moveNext) return;

    onboardingStore.handleNextStep("summarize");
  }
}

onMounted(() => updateStatus());

watch(
  () => onboardingStore.error,
  (error) => {
    if (!error) return;
    status.value = "error";
  }
);

watch(
  () => onboardingStore.uploadedJob,
  () => updateStatus(true)
);
</script>
