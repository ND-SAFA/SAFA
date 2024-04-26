<template>
  <flex-box v-if="hasSummary" justify="between" align="center">
    <typography variant="caption" value="Summary" />
    <text-button
      v-if="!generateApproval && displayActions"
      text
      color="primary"
      :loading="artifactGenerationApiStore.summaryGenLoading"
      :icon="hasSummary ? 'graph-refresh' : 'generate'"
      :label="hasSummary ? 'Resummarize' : 'Summarize'"
      @click="handleGenerateSummary"
    />
    <q-card v-else-if="displayActions" bordered>
      <text-button text icon="save" label="Save" @click="handleSaveSummary" />
      <text-button
        text
        :loading="artifactGenerationApiStore.summaryGenLoading"
        icon="graph-refresh"
        label="Retry"
        @click="handleGenerateSummary"
      />
      <text-button
        text
        icon="delete"
        label="Delete"
        @click="handleDeleteSummary"
      />
    </q-card>
  </flex-box>
  <flex-box full-width>
    <typography
      v-if="hasSummary && !generateApproval"
      default-expanded
      :collapse-length="0"
      variant="expandable"
      :value="summary"
      data-cy="text-selected-body"
    />
    <q-card
      v-else-if="generateApproval"
      bordered
      class="full-width q-pa-sm q-mt-sm"
    >
      <text-input
        v-model="summary"
        label="Generated Summary"
        type="textarea"
        hide-hint
      />
    </q-card>
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays the selected node's summary, and allows for regenerating summaries.
 */
export default {
  name: "ArtifactSummary",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { ENABLED_FEATURES } from "@/util";
import {
  artifactGenerationApiStore,
  artifactStore,
  permissionStore,
} from "@/hooks";
import {
  Typography,
  FlexBox,
  TextButton,
  TextInput,
} from "@/components/common";

const displayActions = computed(
  () =>
    permissionStore.isAllowed("project.generate") &&
    ENABLED_FEATURES.GENERATE_SUMMARIES
);

const artifact = computed(() => artifactStore.selectedArtifact);

const generateConfirmation = computed(
  () => artifactGenerationApiStore.summaryGenConfirm
);

const summary = computed<string>({
  get() {
    return generateConfirmation.value?.summary || artifact.value?.summary || "";
  },
  set(value) {
    if (!generateConfirmation.value) return;

    generateConfirmation.value.summary = value;
  },
});

const hasSummary = computed(() => !!summary.value);
const generateApproval = computed(() => !!generateConfirmation.value);

/**
 * Generates a summary for the artifact.
 */
function handleGenerateSummary(): void {
  if (!artifact.value) return;

  artifactGenerationApiStore.handleGenerateSummary(artifact.value);
}

/**
 * Saves the generated summary for the artifact.
 */
function handleSaveSummary(): void {
  generateConfirmation.value?.confirm();
}

/**
 * Deletes the generated summary for the artifact.
 */
function handleDeleteSummary(): void {
  generateConfirmation.value?.clear();
}

watch(
  () => artifact.value,
  () => generateConfirmation.value?.clear()
);
</script>
