<template>
  <v-text-field
    v-model="model"
    filled
    :label="label"
    data-cy="input-password"
    :error-messages="errors"
    :error="errors && errors.length > 0"
    @keydown.enter="emit('enter')"
  />
</template>

<script lang="ts">
/**
 * A generic text input.
 */
export default {
  name: "TextInput",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";
import { useVModel } from "@/hooks";

const props = defineProps<{
  modelValue: string;
  label?: string;
  errors?: string[];
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "enter"): void;
}>();

const model = useVModel(props, "modelValue");
</script>
