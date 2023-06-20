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
    @filter="filter"
    @popup-show="handleReloadOptions"
  >
    <template #before-options>
      <flex-box full-width justify="end" y="1">
        <type-buttons
          default-visible
          :hidden-types="hiddenTypes"
          @click="handleTypeChange"
        />
      </flex-box>
    </template>
    <template #option="{ opt, itemProps }">
      <artifact-body-display v-bind="itemProps" display-title :artifact="opt" />
    </template>
    <template #selected-item="{ opt, index, removeAtIndex }">
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
 *
 * @emits `input` (Artifact[]) - On input change.
 * @emits `enter` - On submit.
 */
export default {
  name: "ArtifactInput",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactInput, TimArtifactLevelSchema } from "@/types";
import { filterArtifacts } from "@/util";
import { artifactStore, useVModel } from "@/hooks";
import {
  Typography,
  ArtifactBodyDisplay,
  AttributeChip,
  FlexBox,
} from "@/components/common/display";
import { TypeButtons } from "@/components/common/button";

const props = defineProps<ArtifactInput>();

const model = useVModel(props, "modelValue");

const artifacts = computed(() =>
  props.onlyDocumentArtifacts
    ? artifactStore.currentArtifacts
    : artifactStore.allArtifacts
);

const options = ref(artifacts.value);
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
function filter(searchText: string, update: (fn: () => void) => void): void {
  update(() => {
    if (searchText === "") {
      options.value = artifacts.value.filter(
        (artifact) => !hiddenTypes.value.includes(artifact.type)
      );
    } else {
      const lowercaseSearchText = searchText.toLowerCase();

      options.value = artifacts.value.filter(
        (artifact) =>
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
  option: TimArtifactLevelSchema,
  allOptions: TimArtifactLevelSchema[]
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

  filter("", (fn) => fn());
}

/**
 * If default hidden types are set, the artifact list will be re-filtered when opened.
 */
function handleReloadOptions(): void {
  if (!props.defaultHiddenTypes) return;

  hiddenTypes.value = props.defaultHiddenTypes;
  filter("", (fn) => fn());
}
</script>
