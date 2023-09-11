<template>
  <q-select
    v-model="model"
    filled
    label="Model"
    :options="options"
    option-value="id"
    option-label="id"
    map-options
    emit-value
  >
    <template #option="{ opt, itemProps }: { opt: GenerationModelSchema }">
      <list-item v-bind="itemProps" :title="opt.id" :subtitle="opt.name" />
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * A selector for trace generation methods.
 */
export default {
  name: "GenMethodInput",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  GenerationModelSchema,
  GenMethodInputProps,
  ModelType,
  SelectOption,
} from "@/types";
import { createOption } from "@/util";
import { useVModel } from "@/hooks";
import { ListItem } from "@/components/common/display";

const props = defineProps<GenMethodInputProps>();

defineEmits<{
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");

/**
 * @return display names for each trace model type.
 */
function traceModelOptions(): SelectOption<ModelType>[] {
  return [
    createOption(
      "NLBert",
      "Slower, higher quality links. Traces free-text artifacts to other free-text artifacts."
    ),
    createOption(
      "PLBert",
      "Slower, higher quality links. Traces free-text artifacts to source code."
    ),
    createOption(
      "AutomotiveBert",
      "Slower, high quality links for automotive projects."
    ),
    createOption("VSM", "Faster, lower quality links."),
  ];
}

const options = computed(() =>
  props.onlyTrainable ? traceModelOptions().slice(0, 3) : traceModelOptions()
);
</script>
