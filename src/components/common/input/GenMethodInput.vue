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
    <template #option="{ opt, itemProps }">
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
import { traceModelOptions } from "@/util";
import { useVModel } from "@/hooks";
import { ListItem } from "@/components/common/display";

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
