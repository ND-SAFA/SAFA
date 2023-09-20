<template>
  <q-select
    v-model="model"
    filled
    label="Generation Model"
    hint="The model used to generate trace links."
    :options="options"
    option-label="name"
    option-value="id"
    map-options
  >
    <template #option="{ opt, itemProps }: { opt: GenerationModelSchema }">
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
import { CustomModelInputProps, GenerationModelSchema } from "@/types";
import { projectStore, useVModel } from "@/hooks";
import { ListItem } from "@/components/common/display";

const props = defineProps<CustomModelInputProps>();

defineEmits<{
  (e: "update:modelValue", value: GenerationModelSchema | undefined): void;
}>();

const model = useVModel(props, "modelValue");

const options = computed(() => projectStore.models);
</script>
