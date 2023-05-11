<template>
  <panel-card>
    <flex-box align="center" justify="between">
      <div>
        <typography
          ellipsis
          variant="subtitle"
          el="h1"
          :value="name"
          data-cy="text-selected-name"
        />
        <q-tooltip>{{ name }}</q-tooltip>
      </div>
      <attribute-chip
        artifact-type
        :value="type"
        data-cy="text-selected-type"
      />
    </flex-box>

    <separator b="2" />

    <typography variant="caption" value="Body" />
    <typography
      default-expanded
      :variant="variant"
      :value="body"
      data-cy="text-selected-body"
    />

    <flex-box justify="between" align="center">
      <typography variant="caption" value="Summary" />
      <text-button
        v-if="!generateConfirmation"
        text
        color="primary"
        :loading="generateLoading"
        :icon="hasSummary ? 'graph-refresh' : 'add'"
        :label="hasSummary ? 'Resummarize' : 'Summarize'"
        @click="handleGenerateSummary"
      />
      <q-card v-else bordered>
        <text-button text icon="save" label="Save" @click="handleSaveSummary" />
        <text-button
          text
          icon="delete"
          label="Delete"
          @click="handleDeleteSummary"
        />
      </q-card>
    </flex-box>
    <typography
      v-if="hasSummary"
      default-expanded
      variant="expandable"
      :value="summary"
      data-cy="text-selected-body"
    />

    <attribute-list-display :artifact="artifact" />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's title and option buttons.
 */
export default {
  name: "ArtifactFields",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactSummaryConfirmation, ReservedArtifactType } from "@/types";
import { selectionStore } from "@/hooks";
import { handleGenerateArtifactSummary } from "@/api";
import {
  Typography,
  FlexBox,
  AttributeChip,
  PanelCard,
  AttributeListDisplay,
  Separator,
} from "@/components/common";
import TextButton from "@/components/common/button/TextButton.vue";

const generateLoading = ref(false);
const generateConfirmation = ref<ArtifactSummaryConfirmation | undefined>(
  undefined
);

const artifact = computed(() => selectionStore.selectedArtifact);
const name = computed(() => artifact.value?.name || "");
const type = computed(() => artifact.value?.type || "");
const body = computed(() => artifact.value?.body.trim() || "");
const variant = computed(() =>
  type?.value === ReservedArtifactType.github ? "code" : "expandable"
);

const summary = computed(
  () => generateConfirmation.value?.summary || artifact.value?.summary || ""
);
const hasSummary = computed(() => !!summary.value);

/**
 * Generates a summary for the artifact.
 */
function handleGenerateSummary(): void {
  if (!artifact.value) return;

  generateLoading.value = true;

  handleGenerateArtifactSummary(artifact.value, {
    onComplete: () => (generateLoading.value = false),
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
