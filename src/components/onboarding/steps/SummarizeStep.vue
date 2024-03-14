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

  <callout-sub-step
    v-if="status === 'error'"
    status="error"
    :message="ONBOARDING_SUMMARIZE_ERROR"
  />
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
import {
  integrationsStore,
  onboardingApiStore,
  onboardingStore,
} from "@/hooks";
import {
  FlexBox,
  List,
  ListItem,
  Separator,
  TextButton,
  Typography,
} from "@/components/common";
import CalloutSubStep from "./CalloutSubStep.vue";
import JobLoadingSubStep from "./JobLoadingSubStep.vue";

const status = ref<"initial" | "loading" | "success" | "error">("initial");

/**
 * Sets the status to loading and starts a generation job when the user clicks the import button.
 */
function handleGenerate() {
  status.value = "loading";
  onboardingApiStore.handleImportAndSummarize();
}

/**
 * Updates the status when the job changes.
 */
function updateStatus(moveNext?: boolean) {
  const jobStatus = onboardingStore.uploadedJob?.status;

  if (!jobStatus) {
    status.value = "initial";
  } else if (jobStatus === "FAILED" || onboardingStore.error) {
    status.value = "error";
  } else if (jobStatus === "IN_PROGRESS") {
    status.value = "loading";
  } else if (status.value === "loading" && jobStatus === "COMPLETED") {
    status.value = "success";

    if (!moveNext) return;

    onboardingApiStore.handleLoadNextStep("summarize");
  }
}

onMounted(() => updateStatus());

watch(
  () => onboardingStore.error,
  (error) => {
    if (!error) return;
    updateStatus();
  }
);

watch(
  () => onboardingStore.uploadedJob,
  () => updateStatus(true)
);
</script>
