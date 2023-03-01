<template>
  <div>
    <q-tabs v-model="model" active-color="primary">
      <q-tab
        v-for="{ id, name } in tabs"
        :key="id"
        :name="id"
        :label="name"
        no-caps
      />
    </q-tabs>
    <q-tab-panels v-model="model" animated class="bg-transparent">
      <q-tab-panel v-for="{ id } in tabs" :key="id" :name="id" class="q-pt-sm">
        <slot :name="id" />
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script lang="ts">
/**
 * Renders content across multiple tabs.
 * Use the `<v-tab/>` component to wrap each tab's child component.
 */
export default {
  name: "TabList",
};
</script>

<script setup lang="ts">
import { SelectOption } from "@/types";
import { useVModel } from "@/hooks";

const props = defineProps<{
  /**
   * The tab id currently selected.
   */
  modelValue: string;
  /**
   * The tabs to display.
   */
  tabs: SelectOption[];
}>();

defineEmits<{
  (e: "update:modelValue", value: number): void;
}>();

const model = useVModel(props, "modelValue");
</script>
