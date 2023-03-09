<template>
  <q-select
    ref="artifactTypeInput"
    v-model="model"
    filled
    :label="label"
    :multiple="!!multiple"
    :options="options"
    :hint="hint"
    :error-message="errorMessage"
    @popup-hide="emit('blur')"
  >
    <template #selected-item="{ opt }">
      <attribute-chip v-if="!!opt" artifact-type :value="opt" />
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
import { computed, withDefaults } from "vue";
import { artifactStore, typeOptionsStore, useVModel } from "@/hooks";
import { AttributeChip, Typography } from "@/components/common/display";

const props = withDefaults(
  defineProps<{
    modelValue: string[] | string | null;
    multiple?: boolean;
    label?: string;
    hint?: string;
    errorMessage?: string;
    showCount?: boolean;
  }>(),
  {
    label: "Artifact Types",
    multiple: false,
    hint: undefined,
    errorMessage: undefined,
  }
);

const emit = defineEmits<{
  (e: "update:modelValue", value: string[] | string | null): void;
  (e: "blur"): void;
}>();

const model = useVModel(props, "modelValue");

const options = computed(() => typeOptionsStore.artifactTypes);

const optionCount = computed(() =>
  props.showCount && typeof model.value === "string"
    ? artifactStore.getArtifactsByType[model.value]?.length || 0
    : 0
);

const optionCountDisplay = computed(() =>
  optionCount.value === 1 ? "1 Artifact" : `${optionCount.value} Artifacts`
);
</script>
