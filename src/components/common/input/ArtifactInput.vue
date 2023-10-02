<template>
  <q-select
    v-model="model"
    filled
    use-chips
    map-options
    emit-value
    use-input
    :clearable="multiple"
    :multiple="multiple"
    :label="label || 'Artifact'"
    :options="options"
    option-label="name"
    option-value="id"
    input-debounce="0"
    @filter="filterOptions"
    @popup-show="handleReloadOptions"
  >
    <template #before-options>
      <div class="q-py-sm bg-neutral sticky-top">
        <type-buttons
          class="width-fit q-ml-auto"
          default-visible
          :hidden-types="hiddenTypes"
          @click="handleTypeChange"
        />
        <slot name="before-options" />
      </div>
    </template>
    <template #option="{ opt, itemProps }">
      <artifact-body-display v-bind="itemProps" display-title :artifact="opt" />
    </template>
    <template
      #selected-item="{
        opt,
        index,
        removeAtIndex,
      }: {
        opt: ArtifactSchema;
        index: number;
        removeAtIndex(num: number): void;
      }"
    >
      <attribute-chip
        v-if="!!opt && opt.name && index < 3"
        removable
        :value="opt.name"
        @remove="removeAtIndex(index)"
      />
      <typography
        v-else-if="index === 3"
        secondary
        x="2"
        :value="'+' + (selectedCount - 3)"
      />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * An input for artifacts.
 */
export default {
  name: "ArtifactInput",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ArtifactInput, ArtifactSchema, ArtifactTypeSchema } from "@/types";
import { filterArtifacts, sortSelectedArtifactsToTop } from "@/util";
import { artifactStore, useVModel } from "@/hooks";
import { Typography, AttributeChip } from "@/components/common/display";
import { TypeButtons } from "@/components/common/button";
import ArtifactBodyDisplay from "@/components/artifact/display/ArtifactBodyDisplay.vue";

const props = defineProps<ArtifactInput>();

const model = useVModel(props, "modelValue");

const artifacts = computed(() =>
  props.onlyDocumentArtifacts
    ? artifactStore.currentArtifacts
    : artifactStore.allArtifacts
);
const sortedArtifacts = computed(() =>
  sortSelectedArtifactsToTop(artifacts.value, model.value)
);

const options = ref(sortedArtifacts.value);
const hiddenTypes = ref(props.defaultHiddenTypes || []);

const selectedCount = computed(() => {
  if (typeof model.value === "string") {
    return 1;
  } else if (Array.isArray(model.value)) {
    return model.value.length;
  } else {
    return 0;
  }
});

/**
 * Filters the artifact options.
 * @param searchText - The search text to filter with.
 * @param update - A function call to update the options.
 */
function filterOptions(
  searchText: string,
  update: (fn: () => void) => void
): void {
  update(() => {
    if (searchText === "") {
      options.value = sortedArtifacts.value.filter(
        (artifact) =>
          !props.hiddenArtifactIds?.includes(artifact.id) &&
          !hiddenTypes.value.includes(artifact.type)
      );
    } else {
      const lowercaseSearchText = searchText.toLowerCase();

      options.value = sortedArtifacts.value.filter(
        (artifact) =>
          !props.hiddenArtifactIds?.includes(artifact.id) &&
          !hiddenTypes.value.includes(artifact.type) &&
          filterArtifacts(artifact, lowercaseSearchText)
      );
    }
  });
}

/**
 * Toggles whether a type is visible in the artifact list.
 * @param option - The type to toggle.
 * @param allOptions - All possible types.
 */
function handleTypeChange(
  option: ArtifactTypeSchema,
  allOptions: ArtifactTypeSchema[]
): void {
  if (hiddenTypes.value.length === 0) {
    hiddenTypes.value = allOptions
      .map((type) => type.name)
      .filter((type) => type !== option.name);
  } else if (hiddenTypes.value.find((type) => type === option.name)) {
    hiddenTypes.value = hiddenTypes.value.filter(
      (type) => type !== option.name
    );
  } else {
    hiddenTypes.value.push(option.name);
  }

  if (hiddenTypes.value.length === allOptions.length) {
    hiddenTypes.value = [];
  }

  filterOptions("", (fn) => fn());
}

/**
 * If default hidden types are set, the artifact list will be re-filtered when opened.
 */
function handleReloadOptions(): void {
  if (!props.defaultHiddenTypes) return;

  hiddenTypes.value = props.defaultHiddenTypes;
  filterOptions("", (fn) => fn());
}

// When the model changes, filter selected options to the top.
watch(
  () => model.value,
  () => (options.value = sortSelectedArtifactsToTop(options.value, model.value))
);
</script>
