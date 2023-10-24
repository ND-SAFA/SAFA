<template>
  <q-tabs
    v-model="model"
    active-color="primary"
    align="left"
    :breakpoint="0"
    :vertical="props.vertical"
    :class="props.class"
  >
    <slot name="before" />
    <q-tab
      v-for="{ id, name } in tabs"
      :key="id"
      :name="id"
      :label="name"
      no-caps
    />
    <slot name="after" />
  </q-tabs>
  <separator v-if="props.vertical" vertical class="q-mr-md" />
  <q-tab-panels
    v-model="model"
    animated
    class="bg-transparent full-width"
    :vertical="props.vertical"
    :transition-prev="props.vertical ? 'jump-up' : undefined"
    :transition-next="props.vertical ? 'jump-down' : undefined"
  >
    <q-tab-panel
      v-for="{ id } in tabs"
      :key="id"
      :name="id"
      class="q-pt-sm q-px-none"
    >
      <slot :name="id" />
    </q-tab-panel>
  </q-tab-panels>
</template>

<script lang="ts">
/**
 * Renders content across multiple tabs.
 */
export default {
  name: "TabList",
};
</script>

<script setup lang="ts">
import { TabListProps } from "@/types";
import { useVModel } from "@/hooks";
import { Separator } from "@/components";

const props = defineProps<TabListProps>();

defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const model = useVModel(props, "modelValue");
</script>
