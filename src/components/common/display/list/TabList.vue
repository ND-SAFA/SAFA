<template>
  <div>
    <flex-box class="width-fit" align="center">
      <slot name="before" />
      <v-tabs v-model="model" class="transparent-bg">
        <v-tab v-for="{ name } in tabs" :key="name" class="transparent-bg">
          <typography :value="name" />
        </v-tab>
      </v-tabs>
      <slot name="after" />
    </flex-box>
    <v-tabs v-model="model" class="mt-1">
      <slot />
    </v-tabs>
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
import { ref, watch, defineProps, defineEmits } from "vue";
import { SelectOption } from "@/types";
import { FlexBox } from "@/components/common/layout";
import Typography from "../Typography.vue";

const props = defineProps<{
  modelValue: number;
  tabs: SelectOption[];
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: number): void;
}>();

const model = ref(props.modelValue);

watch(
  () => model.value,
  () => emit("update:modelValue", model.value)
);
</script>
