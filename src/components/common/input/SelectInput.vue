<template>
  <q-select
    v-model="model"
    :filled="!props.outlined"
    :outlined="props.outlined"
    :disable="props.disabled"
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
import { SelectInputProps } from "@/types";
import { useVModel } from "@/hooks";

const props = defineProps<SelectInputProps>();

defineEmits<{
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");
</script>
