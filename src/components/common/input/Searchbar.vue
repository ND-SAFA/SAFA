<template>
  <q-input
    v-model="model"
    dense
    outlined
    clearable
    :label="props.label"
    :hint="props.hint"
    class="full-width"
    @keydown="handleKeydown"
  >
    <template #append>
      <slot name="append" :search="model as string" />
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
import { withDefaults } from "vue";
import { SearchbarProps } from "@/types";
import { useVModel } from "@/hooks";
import { Icon } from "@/components/common/display";

const props = withDefaults(defineProps<SearchbarProps>(), { label: "Search" });

const emit = defineEmits<{
  /**
   * Called when the model is updated.
   */
  (e: "update:modelValue"): void;
  /**
   * Called when the enter button is pressed.
   */
  (e: "enter"): void;
}>();

const model = useVModel(props, "modelValue");

/**
 * Emits an event when enter is clicked.
 */
function handleKeydown(e?: { key: string }) {
  if (e?.key === "Enter") {
    emit("enter");
  }
}
</script>
