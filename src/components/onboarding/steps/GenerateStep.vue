<template>
  <typography
    v-if="status !== 'success'"
    el="div"
    :value="ONBOARDING_GENERATE_MESSAGE"
  />
  <typography
    v-if="status !== 'success'"
    el="div"
    secondary
    :value="ONBOARDING_GENERATE_DURATION"
  />
  <callout-sub-step
    v-if="status === 'success'"
    icon="success"
    :message="ONBOARDING_GENERATE_SUCCESS"
  />

  <flex-box v-if="status === 'initial'" column align="center" t="4">
    <callout-sub-step
      v-if="onboardingStore.blockGeneration"
      icon="payment"
      :message="ONBOARDING_GENERATE_LARGE"
    />
    <list v-else class="full-width">
      <list-item
        color="primary"
        title="Project Size"
        :subtitle="codeFiles"
        icon="code"
      />
      <separator inset />
      <list-item
        color="primary"
        title="Generating Documents"
        :subtitle="onboardingStore.generationTypes.join(', ')"
        icon="create-artifact"
      />
      <separator v-if="onboardingStore.cost" inset />
      <list-item
        v-if="onboardingStore.cost"
        color="primary"
        title="Generation Cost"
        :subtitle="generateCost"
        icon="payment"
      />
    </list>

    <flex-box t="4">
      <text-button
        text
        color="gradient"
        class="bd-gradient"
        icon="generate-artifacts"
        :disabled="onboardingStore.blockGeneration || onboardingStore.error"
        @click="onboardingStore.handleGenerateDocumentation"
      >
        {{ generateLabel }}
      </text-button>
    </flex-box>
  </flex-box>

  <job-loading-sub-step v-if="status === 'loading'" />

  <flex-box v-if="status === 'success'" column align="center" t="4">
    <text-button
      text
      color="gradient"
      class="bd-gradient"
      icon="download"
      :loading="projectApiStore.saveProjectLoading"
      @click="onboardingStore.handleExportProject"
    >
      Export as CSV
    </text-button>
    <flex-box align="center" justify="center" full-width>
      <separator style="width: 40px" />
      <typography secondary el="div" class="q-ma-sm" value="OR" />
      <separator style="width: 40px" />
    </flex-box>
    <text-button
      text
      color="gradient"
      class="bd-gradient"
      icon="view-tree"
      @click="onboardingStore.handleViewProject"
    >
      View in SAFA
    </text-button>
  </flex-box>

  <callout-sub-step
    v-if="status === 'error'"
    icon="error"
    error
    :message="ONBOARDING_GENERATE_ERROR"
  />
</template>

<script lang="ts">
/**
 * The onboarding step to generate data.
 */
export default {
  name: "GenerateStep",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import {
  ONBOARDING_GENERATE_DURATION,
  ONBOARDING_GENERATE_ERROR,
  ONBOARDING_GENERATE_LARGE,
  ONBOARDING_GENERATE_MESSAGE,
  ONBOARDING_GENERATE_SUCCESS,
} from "@/util";
import { artifactStore, onboardingStore, projectApiStore } from "@/hooks";
import {
  FlexBox,
  Separator,
  TextButton,
  Typography,
  List,
  ListItem,
} from "@/components/common";
import CalloutSubStep from "./CalloutSubStep.vue";
import JobLoadingSubStep from "./JobLoadingSubStep.vue";

const status = ref<"initial" | "loading" | "success" | "error">("initial");

const codeFiles = computed(() => artifactStore.allArtifacts.length + " Files");
const generateCost = computed(() =>
  onboardingStore.cost ? `$${Math.floor(onboardingStore.cost)}.00` : ""
);

const generateLabel = computed(() =>
  onboardingStore.displayBilling
    ? "Checkout & Generate"
    : "Generate Documentation"
);

/**
 * Updates the status when the job changes.
 */
function updateStatus() {
  // Skip jobs that are not for generation.
  if (!onboardingStore.uploadedJob?.steps.includes("Generating Artifacts")) {
    return;
  }

  if (onboardingStore.uploadedJob?.status === "IN_PROGRESS") {
    status.value = "loading";
  }
  if (onboardingStore.uploadedJob?.status === "FAILED") {
    status.value = "error";
  } else if (onboardingStore.uploadedJob?.status === "COMPLETED") {
    status.value = "success";
    onboardingStore.steps[onboardingStore.steps.length - 1].done = true;
  }
}

onMounted(updateStatus);

watch(
  () => onboardingStore.error,
  (error) => {
    if (!error) return;
    status.value = "error";
  }
);

watch(() => onboardingStore.uploadedJob, updateStatus);
</script>
