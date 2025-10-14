<template>
  <details-panel panel="generateArtifact">
    <panel-card title="Generate Artifacts" borderless>
      <q-btn-group flat class="q-mb-md">
        <text-button
          v-bind="buttonProps('single')"
          label="Single"
          icon="artifact"
          @click="mode = 'single'"
        />
        <text-button
          v-bind="buttonProps('multiple')"
          label="Multiple"
          icon="nav-artifact"
          @click="mode = 'multiple'"
        />
      </q-btn-group>

      <div v-if="mode === 'single'" class="q-mb-md">
        <artifact-input
          v-model="childArtifactIds"
          multiple
          label="Child Artifacts"
          hint="Generate a single parent artifact for these artifacts."
        />
      </div>
      <div v-else class="q-mb-md">
        <artifact-type-input
          v-model="childArtifactTypes"
          multiple
          label="Child Artifact Types"
          hint="Generate multiple parent artifacts by clustering these types of artifacts by functionality."
        />
      </div>
      <multiselect-input
        v-model="parentArtifactTypes"
        :options="ARTIFACT_GENERATION_OPTIONS"
        label="Parent Artifact Types"
        hint="The type of parent artifacts to create. If multiple are selected, each type will be sequentially generated based on the past type."
      />

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
 * Displays inputs for generating new parent artifacts based on child artifacts.
 */
export default {
  name: "ArtifactGenerationPanel",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { GenerateArtifactSchema } from "@/types";
import { ARTIFACT_GENERATION_OPTIONS } from "@/util";
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
  MultiselectInput,
} from "@/components/common";

const mode = ref<"single" | "multiple">("single");
const childArtifactIds = ref<string[]>([]);
const childArtifactTypes = ref<string[]>([]);
const parentArtifactTypes = ref<string[]>([]);

const canGenerate = computed(() => {
  if (mode.value === "single") {
    return (
      childArtifactIds.value.length > 0 && parentArtifactTypes.value.length > 0
    );
  } else {
    return (
      childArtifactTypes.value.length > 0 &&
      parentArtifactTypes.value.length > 0
    );
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
    childArtifactIds.value = selectionStore.selectedGroupIds;
    childArtifactTypes.value = [];
  } else if (timStore.selectedArtifactLevel) {
    mode.value = "multiple";
    childArtifactTypes.value = [timStore.selectedArtifactLevel.name];
    childArtifactIds.value = [];
  } else {
    mode.value = "single";
    childArtifactIds.value = [];
    childArtifactTypes.value = [];
  }

  parentArtifactTypes.value = [];
}

/**
 * Generates new parent artifacts based on inputted child artifacts.
 */
function handleGenerate(): void {
  const config: GenerateArtifactSchema =
    mode.value === "single"
      ? {
          artifacts: childArtifactIds.value,
          targetTypes: parentArtifactTypes.value,
          clusters: [childArtifactIds.value],
        }
      : {
          artifacts: artifactStore.allArtifacts
            .filter(({ type }) => childArtifactTypes.value.includes(type))
            .map(({ id }) => id),
          targetTypes: parentArtifactTypes.value,
        };

  artifactGenerationApiStore.handleGenerateArtifacts(config, {
    onSuccess: () => {
      handleReset();
      appStore.closeSidePanels();
    },
  });
}
watch(
  () => appStore.popups.detailsPanel === "generateArtifact",
  (openState) => {
    if (!openState) return;

    handleReset();
  }
);
</script>
