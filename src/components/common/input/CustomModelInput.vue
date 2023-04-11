<template>
  <q-select
    v-model="model"
    filled
    label="Custom Model"
    :options="options"
    option-label="name"
    option-value="id"
    map-options
  >
    <template #option="{ opt, itemProps }">
      <list-item
        v-bind="itemProps"
        :title="opt.name"
        :subtitle="opt.baseModel"
      />
    </template>
  </q-select>
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
import { computed } from "vue";
import { GenerationModelSchema } from "@/types";
import { projectStore, useVModel } from "@/hooks";
import { ListItem } from "@/components/common/display";

const props = defineProps<{
  modelValue: GenerationModelSchema | undefined;
}>();

defineEmits<{
  (e: "update:modelValue", value: GenerationModelSchema | undefined): void;
}>();

const model = useVModel(props, "modelValue");

const options = computed(() => projectStore.models);
</script>
