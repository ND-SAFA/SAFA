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
    @blur="emit('blur')"
    @submit="emit('blur')"
  >
    <template #selected-item="{ opt }">
      <attribute-chip artifact-type :value="opt" />
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
import { typeOptionsStore, useVModel } from "@/hooks";
import { AttributeChip } from "@/components/common/display";

const props = withDefaults(
  defineProps<{
    modelValue: string[] | string | null;
    multiple?: boolean;
    label?: string;
    hint?: string;
    errorMessage?: string;
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
</script>
