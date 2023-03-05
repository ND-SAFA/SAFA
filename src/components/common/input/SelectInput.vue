<template>
  <q-select
    v-model="model"
    :filled="!props.outlined"
    :outlined="props.outlined"
    :label="props.label"
    :options="props.options"
    :option-value="props.optionValue"
    :option-label="props.optionLabel"
    :map-options="props.optionToValue"
    :emit-value="props.optionToValue"
  >
    <template #prepend>
      <slot name="prepend" />
    </template>
  </q-select>
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
  /**
   * The key of an option's id.
   */
  optionValue?: string;
  /**
   * The key of an option's display label.
   */
  optionLabel?: string;
  /**
   * Only saves the option's value, not the entire object.
   */
  optionToValue?: boolean;
  /**
   * Whether to display as outlined, instead of the default filled.
   */
  outlined?: boolean;
}>();

defineEmits<{
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");
</script>
