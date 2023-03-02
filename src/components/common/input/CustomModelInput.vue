<template>
  <q-select
    v-model="model"
    filled
    label="Custom Model"
    :items="options"
    option-label="name"
    option-value="id"
  >
    <template #option="{ opt }">
      <div class="q-my-sm">
        <typography el="div" :value="opt.name" />
        <typography variant="caption" :opt="item.baseModel" />
      </div>
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
import { Typography } from "@/components/common/display";

const props = defineProps<{
  modelValue: GenerationModelSchema | undefined;
}>();

defineEmits<{
  (e: "update:modelValue", value: GenerationModelSchema | undefined): void;
}>();

const model = useVModel(props, "modelValue");

const options = computed(() => projectStore.models);
</script>
