<template>
  <q-select
    ref="artifactTypeInput"
    v-model="model"
    filled
    :label="label"
    :multiple="multiple"
    :options="options"
    :hint="hint"
    :error-message="errorMessage || undefined"
    :dense="props.dense"
    use-input
    new-value-mode="add-unique"
    input-debounce="0"
    @filter="filter"
    @popup-hide="emit('blur')"
  >
    <template #selected-item="{ opt }">
      <attribute-chip
        v-if="!!opt"
        artifact-type
        :value="opt"
        :dense="props.dense"
      />
      <typography v-if="optionCount > 0" l="1" :value="optionCountDisplay" />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * An input for selecting artifact types.
 */
export default {
  name: "ArtifactTypeInput",
};
</script>

<script setup lang="ts">
import { computed, ref, watch, withDefaults } from "vue";
import { ArtifactTypeInputProps } from "@/types";
import { artifactStore, timStore, useVModel } from "@/hooks";
import { AttributeChip, Typography } from "@/components/common/display";

const props = withDefaults(defineProps<ArtifactTypeInputProps>(), {
  label: "Artifact Types",
  multiple: false,
  hint: undefined,
  errorMessage: undefined,
});

const emit = defineEmits<{
  (e: "update:modelValue", value: string[] | string | null): void;
  (e: "blur"): void;
}>();

const model = useVModel(props, "modelValue");

const options = ref(timStore.typeNames);

const optionCount = computed(() =>
  props.showCount && typeof model.value === "string"
    ? artifactStore.artifactsByType.get(model.value)?.length || 0
    : 0
);

const optionCountDisplay = computed(() =>
  optionCount.value === 1 ? "1 Artifact" : `${optionCount.value} Artifacts`
);

/**
 * Filters the artifact type options.
 * @param searchText - The search text to filter with.
 * @param update - A function call to update the options.
 */
function filter(
  searchText: string | null,
  update: (fn: () => void) => void
): void {
  update(() => {
    if (!searchText) {
      options.value = timStore.typeNames;
    } else {
      const lowercaseSearchText = searchText.toLowerCase();

      options.value = timStore.typeNames.filter((type) =>
        (type?.toLowerCase() || "").includes(lowercaseSearchText)
      );
    }
  });
}

watch(
  () => timStore.typeNames,
  (typeNames) => (options.value = typeNames)
);
</script>
