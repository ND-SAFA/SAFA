<template>
  <typography el="div" :value="ONBOARDING_SUMMARIZE_MESSAGE" />
  <typography el="div" secondary :value="ONBOARDING_SUMMARIZE_DURATION" />

  <flex-box v-if="status === 'initial'" column align="center" t="4">
    <list class="full-width">
      <list-item
        color="primary"
        title="Importing From GitHub"
        :subtitle="integrationsStore.gitHubFullProjectName"
        icon="project-add"
      />
      <separator inset />
      <list-item
        color="primary"
        title="Generating Data"
        subtitle="Project Summary, File Summaries"
        icon="create-artifact"
      />
    </list>

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
    <typography :value="ONBOARDING_SUMMARIZE_ERROR" />
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
import {
  ONBOARDING_SUMMARIZE_DURATION,
  ONBOARDING_SUMMARIZE_ERROR,
  ONBOARDING_SUMMARIZE_MESSAGE,
} from "@/util";
import { integrationsStore, onboardingStore } from "@/hooks";
import {
  FlexBox,
  Icon,
  List,
  ListItem,
  Separator,
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
