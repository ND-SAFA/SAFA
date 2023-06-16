<template>
  <flex-box justify="between" align="center">
    <typography variant="caption" value="Summary" />
    <text-button
      v-if="!generateApproval"
      text
      color="primary"
      :loading="artifactGenerationApiStore.summaryGenLoading"
      :icon="hasSummary ? 'graph-refresh' : 'add'"
      :label="hasSummary ? 'Resummarize' : 'Summarize'"
      @click="handleGenerateSummary"
    />
    <q-card v-else bordered>
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
import { computed, ref } from "vue";
import { ArtifactSummaryConfirmation } from "@/types";
import { artifactGenerationApiStore, selectionStore } from "@/hooks";
import { Typography, FlexBox, TextButton } from "@/components/common";
import TextInput from "@/components/common/input/TextInput.vue";

const generateConfirmation = ref<ArtifactSummaryConfirmation | undefined>(
  undefined
);

const artifact = computed(() => selectionStore.selectedArtifact);

const summary = computed({
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

  artifactGenerationApiStore.handleGenerateSummary(artifact.value, {
    onSuccess: (confirmation) => (generateConfirmation.value = confirmation),
  });
}

/**
 * Saves the generated summary for the artifact.
 */
function handleSaveSummary(): void {
  if (!generateConfirmation.value) return;

  generateConfirmation.value.confirm();
  generateConfirmation.value = undefined;
}

/**
 * Deletes the generated summary for the artifact.
 */
function handleDeleteSummary(): void {
  generateConfirmation.value = undefined;
}
</script>
