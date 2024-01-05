<template>
  <typography
    v-if="status !== 'success'"
    el="div"
    value="
      Now that your code has been imported and summarized,
      we can generate additional documentation to group related functionality.
      You will receive an email when the import completes.
    "
  />
  <typography
    v-if="status !== 'success'"
    el="div"
    secondary
    value="This process may take an additional 30 minutes depending on the size of your project."
  />
  <typography
    v-if="status === 'success'"
    el="div"
    value="
      Your documentation is ready!
      You can either export the documentation, or view the data in SAFA's knowledge graph below.
    "
  />

  <flex-box v-if="status === 'initial'" column align="center" t="4">
    <list class="full-width">
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
        :disabled="onboardingStore.error"
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

  <q-banner v-if="status === 'error'" rounded class="bg-background q-mt-md">
    <template #avatar>
      <icon variant="error" color="secondary" size="md" class="q-mr-sm" />
    </template>
    <typography
      value="
          On no! It looks like there was an issue with generating documentation.
          You can schedule a call with us below to ensure your data gets generated properly.
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
 * The onboarding step to generate data.
 */
export default {
  name: "GenerateStep",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { artifactStore, onboardingStore, projectApiStore } from "@/hooks";
import {
  FlexBox,
  Icon,
  Separator,
  TextButton,
  Typography,
  List,
  ListItem,
} from "@/components/common";
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
