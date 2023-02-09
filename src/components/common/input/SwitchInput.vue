<template>
  <v-switch v-model="model" inset :label="label" class="mr-2" />
</template>

<script lang="ts">
/**
 * Displays a generic switch input.
 */
export default {
  name: "SwitchInput",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits } from "vue";

import { useVModel } from "@/hooks";

const props = defineProps<{
  modelValue: boolean;
  label: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const model = useVModel(props, "modelValue");
</script>
