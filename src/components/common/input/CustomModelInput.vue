<template>
  <v-select
    v-model="model"
    filled
    hide-details
    label="Custom Model"
    :items="projectStore.models"
    class="mr-2"
    item-text="name"
    item-value="id"
  >
    <template #item="{ item }">
      <div class="my-1">
        <typography el="div" :value="item.name" />
        <typography variant="caption" :value="item.baseModel" />
      </div>
    </template>
  </v-select>
</template>

<script lang="ts">
/**
 * A selector for custom models.
 */
export default {
  name: "CustomModelInput",
};
</script>

<script setup lang="ts">
import { defineProps, defineEmits, computed } from "vue";
import { GenerationModelSchema } from "@/types";
import { projectStore } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = defineProps<{
  modelValue?: GenerationModelSchema;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: GenerationModelSchema | undefined): void;
  (e: "enter"): void;
}>();

const model = computed({
  get() {
    return props.modelValue?.id;
  },
  set(value) {
    emit(
      "update:modelValue",
      projectStore.models.find(({ id }) => id === value)
    );
  },
});
</script>
