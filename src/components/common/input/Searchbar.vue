<template>
  <q-input v-model="model" outlined clearable :label="label" class="full-width">
    <template #prepend>
      <icon variant="search" />
    </template>
  </q-input>
</template>

<script lang="ts">
/**
 * Searchbar
 */
export default {
  name: "Searchbar",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits, withDefaults } from "vue";
import { useVModel } from "@/hooks";
import Icon from "@/components/common/display/icon/Icon.vue";

const props = withDefaults(
  defineProps<{
    modelValue: string;
    label?: string;
  }>(),
  { label: "Search" }
);

defineEmits<{
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");
</script>
