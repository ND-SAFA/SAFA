<template>
  <q-select
    v-model="model"
    filled
    label="Model"
    :items="options"
    option-value="id"
  >
    <template #option="{ opt, itemProps }">
      <div class="q-my-sm" v-bind="itemProps">
        <typography el="div" :value="opt.id" />
        <typography variant="caption" :value="opt.name" />
      </div>
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
import { traceModelOptions } from "@/util";
import { useVModel } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = defineProps<{
  modelValue?: string;
  onlyTrainable?: boolean;
}>();

defineEmits<{
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");

const options = computed(() =>
  props.onlyTrainable ? traceModelOptions().slice(0, 3) : traceModelOptions()
);
</script>
