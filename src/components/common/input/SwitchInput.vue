<template>
  <q-toggle v-model="model">
    <typography :value="label" />
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
import { useVModel } from "@/hooks";
import Typography from "@/components/common/display/Typography.vue";

const props = defineProps<{
  modelValue: boolean;
  label: string;
}>();

defineEmits<{
  (e: "update:modelValue", value: boolean): void;
}>();

const model = useVModel(props, "modelValue");
</script>
