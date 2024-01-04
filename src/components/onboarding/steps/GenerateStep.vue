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
    <typography el="div" value="Project Size:" />
    <attribute-chip :value="codeFiles" icon="code" color="primary" />
    <typography el="div" value="Generating Documents:" class="q-mt-md" />
    <attribute-chip
      v-for="type in onboardingStore.generationTypes"
      :key="type"
      :value="type"
      icon="create-artifact"
      color="primary"
    />
    <typography
      v-if="onboardingStore.cost"
      class="q-mt-md"
      el="div"
      value="Generation Cost:"
    />
    <attribute-chip
      v-if="onboardingStore.cost"
      :value="'$' + onboardingStore.cost"
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
  AttributeChip,
  FlexBox,
  Icon,
  Separator,
  TextButton,
  Typography,
} from "@/components/common";
import JobLoadingSubStep from "./JobLoadingSubStep.vue";

const codeFiles = ref(artifactStore.allArtifacts.length + " Files");

const status = ref<"initial" | "loading" | "success" | "error">("initial");

const generateLabel = computed(() =>
  onboardingStore.displayBilling
    ? "Checkout & Generate"
    : "Generate Documentation"
);

/**
 * Sets the status to loading and starts a generation job when the user clicks the import button.
 */
function handleGenerate() {
  status.value = "loading";
  onboardingStore.handleGenerateDocumentation();
}

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
