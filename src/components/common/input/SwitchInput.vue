<template>
  <q-toggle v-model="model" :color="props.color">
    <typography :value="props.label" :color="props.color" />
  </q-toggle>
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
import { ThemeColor } from "@/types";
import { useVModel } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = defineProps<{
  modelValue: boolean;
  label: string;
  color?: ThemeColor;
}>();

defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const model = useVModel(props, "modelValue");
</script>
