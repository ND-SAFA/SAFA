<template>
  <q-select
    v-model="model"
    filled
    :label="props.label"
    :options="props.options"
    :option-value="props.optionValue"
    :option-label="props.optionLabel"
  />
</template>

<script lang="ts">
/**
 * A generic select input.
 */
export default {
  name: "SelectInput",
};
</script>

<script setup lang="ts">
import { useVModel } from "@/hooks";

const props = defineProps<{
  label: string;
  modelValue?: unknown;
  options: unknown[];
  optionValue?: string;
  optionLabel?: string;
}>();

defineEmits<{
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");
</script>
