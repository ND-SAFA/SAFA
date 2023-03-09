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
    @filter="filter"
  >
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
import { filterArtifacts } from "@/util";
import { artifactStore, useVModel } from "@/hooks";
import {
  Typography,
  ArtifactBodyDisplay,
  AttributeChip,
} from "@/components/common/display";

const props = defineProps<{
  modelValue: string[] | string | undefined;
  multiple?: boolean;
  label?: string;
  onlyDocumentArtifacts?: boolean;
}>();

const model = useVModel(props, "modelValue");

const artifacts = computed(() =>
  props.onlyDocumentArtifacts
    ? artifactStore.currentArtifacts
    : artifactStore.allArtifacts
);

const options = ref(artifacts.value);

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
      options.value = artifacts.value;
    } else {
      const lowercaseSearchText = searchText.toLowerCase();

      options.value = artifacts.value.filter((artifact) =>
        filterArtifacts(artifact, lowercaseSearchText)
      );
    }
  });
}
</script>
