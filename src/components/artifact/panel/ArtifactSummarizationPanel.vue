<template>
  <details-panel panel="summarizeArtifact">
    <panel-card title="Generate Summaries" borderless>
      <q-btn-group flat class="q-mb-md">
        <text-button
          v-bind="buttonProps('single')"
          label="Artifacts"
          icon="artifact"
          @click="mode = 'single'"
        />
        <text-button
          v-bind="buttonProps('multiple')"
          label="Artifact Types"
          icon="view-tim"
          @click="mode = 'multiple'"
        />
      </q-btn-group>

      <div v-if="mode === 'single'" class="q-mb-md">
        <artifact-input
          v-model="artifactIds"
          multiple
          label="Artifacts"
          hint="Summarize the contents of each artifact listed."
        />
      </div>
      <div v-else class="q-mb-md">
        <artifact-type-input
          v-model="artifactTypes"
          multiple
          label="Artifact Types"
          hint="Summarize the contents of all artifacts of the selected types."
        />
      </div>

      <flex-box full-width justify="end" t="3">
        <text-button
          :disabled="!canGenerate"
          :loading="artifactGenerationApiStore.artifactGenLoading"
          label="Generate"
          color="primary"
          @click="handleGenerate"
        />
      </flex-box>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays inputs for summarizing artifacts.
 */
export default {
  name: "ArtifactSummarizationPanel",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import {
  appStore,
  artifactGenerationApiStore,
  artifactStore,
  selectionStore,
  timStore,
} from "@/hooks";
import {
  DetailsPanel,
  PanelCard,
  FlexBox,
  TextButton,
  ArtifactInput,
  ArtifactTypeInput,
} from "@/components/common";

const mode = ref<"single" | "multiple">("single");
const artifactIds = ref<string[]>([]);
const artifactTypes = ref<string[]>([]);

const canGenerate = computed(() => {
  if (mode.value === "single") {
    return artifactIds.value.length > 0;
  } else {
    return artifactTypes.value.length > 0;
  }
});

/**
 * Returns props for a mode button.
 * @param option - The mode button to get props for.
 */
function buttonProps(option: "single" | "multiple") {
  const selected = mode.value === option;

  return {
    text: !selected,
    color: selected ? undefined : "text",
    class: selected ? "button-group-selected text-primary" : "",
  };
}

/**
 * Clears all input fields.
 */
function handleReset(): void {
  if (selectionStore.selectedGroupIds.length > 0) {
    mode.value = "single";
    artifactIds.value = selectionStore.selectedGroupIds;
    artifactTypes.value = [];
  } else if (timStore.selectedArtifactLevel) {
    mode.value = "multiple";
    artifactTypes.value = [timStore.selectedArtifactLevel.name];
    artifactIds.value = [];
  } else {
    mode.value = "single";
    artifactIds.value = [];
    artifactTypes.value = [];
  }
}

/**
 * Generates new parent artifacts based on inputted child artifacts.
 */
function handleGenerate(): void {
  const ids: string[] =
    mode.value === "single"
      ? artifactIds.value
      : artifactTypes.value
          .map((type) => artifactStore.getArtifactsByType(type))
          .flatMap<string, string[]>(
            (artifacts) => artifacts.map(({ id }) => id),
            []
          );

  artifactGenerationApiStore.handleGenerateAllSummaries(ids, {
    onSuccess: () => {
      handleReset();
      appStore.closeSidePanels();
    },
  });
}

watch(
  () => appStore.popups.detailsPanel === "summarizeArtifact",
  (openState) => {
    if (!openState) return;

    handleReset();
  }
);
</script>
