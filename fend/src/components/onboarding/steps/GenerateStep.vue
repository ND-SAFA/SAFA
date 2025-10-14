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
        :subtitle="ARTIFACT_GENERATION_ONBOARDING.join(', ')"
        icon="create-artifact"
      />
      <separator v-if="onboardingStore.displayBilling" inset />
      <list-item
        v-if="onboardingStore.displayBilling"
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
        @click="onboardingApiStore.handleGenerateDocumentation()"
      >
        {{ generateLabel }}
      </text-button>
    </flex-box>
  </flex-box>

  <job-loading-sub-step v-if="status === 'loading'" />

  <flex-box v-if="status === 'success'" column align="center" y="4">
    <text-button
      text
      color="gradient"
      class="bd-gradient"
      icon="download"
      :loading="projectApiStore.saveProjectLoading"
      @click="onboardingApiStore.handleCloseOnboarding('export')"
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
      @click="onboardingApiStore.handleCloseOnboarding('view')"
    >
      View in SAFA
    </text-button>
  </flex-box>

  <callout-sub-step
    v-if="status === 'success'"
    status="success"
    :message="ONBOARDING_GENERATE_SUCCESS"
  />
  <callout-sub-step
    v-if="status === 'error'"
    status="error"
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
  ARTIFACT_GENERATION_ONBOARDING,
  ONBOARDING_GENERATE_DURATION,
  ONBOARDING_GENERATE_ERROR,
  ONBOARDING_GENERATE_LARGE,
  ONBOARDING_GENERATE_MESSAGE,
  ONBOARDING_GENERATE_SUCCESS,
} from "@/util";
import {
  artifactStore,
  onboardingApiStore,
  onboardingStore,
  projectApiStore,
} from "@/hooks";
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

const fileCount = computed(() => artifactStore.allArtifacts.length);
const totalArtifactCount = computed(() => onboardingStore.cost?.credits || 0);
const documentCount = computed(
  () => totalArtifactCount.value - fileCount.value
);

const codeFiles = computed(
  () =>
    `${fileCount.value} Files | ${documentCount.value} Generated Documents (Estimate)`
);

const dollars = computed(() =>
  onboardingStore.cost ? Math.floor(onboardingStore.cost.price / 100) : 0
);
const cents = computed(() =>
  onboardingStore.cost
    ? String(Math.floor(onboardingStore.cost.price % 100)).padStart(2, "0")
    : "00"
);
const generateCost = computed(() =>
  onboardingStore.cost
    ? `$${dollars.value}.${cents.value} (80% Early Access Discount)`
    : ""
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
  const jobStatus = onboardingStore.uploadedJob?.status;
  const correctJobType = onboardingStore.isGenerationJob;

  if ((correctJobType && jobStatus === "FAILED") || onboardingStore.error) {
    status.value = "error";
  } else if (correctJobType && jobStatus === "IN_PROGRESS") {
    status.value = "loading";
  } else if (
    (correctJobType && jobStatus === "COMPLETED") ||
    onboardingStore.generationCompleted
  ) {
    status.value = "success";
    onboardingStore.generationCompleted = true;
  }
}

onMounted(updateStatus);

watch(
  () => onboardingStore.error,
  (error) => {
    if (!error) return;
    updateStatus();
  }
);

watch(() => onboardingStore.uploadedJob, updateStatus);
</script>
