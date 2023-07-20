<template>
  <q-card flat bordered :class="className" :style="cardStyle">
    <div class="cy-node-title">
      <typography variant="subtitle" :value="props.title" bold />
    </div>

    <separator :style="separatorStyle" class="cy-node-separator q-my-sm" />

    <div v-if="!!props.subtitle" class="cy-node-subtitle">
      <typography variant="subtitle" :value="props.subtitle" />
    </div>

    <typography v-if="!!props.body" :value="props.body" />

    <slot />
  </q-card>
</template>

<script lang="ts">
/**
 * A generic node display for the graph.
 */
export default {
  name: "NodeDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { GraphMode } from "@/types";
import { Separator, Typography } from "@/components/common";

const props = defineProps<{
  /**
   * The type of node to display.
   */
  variant: GraphMode;
  /**
   * The color of the node to display.
   */
  color: string;
  /**
   * The title of the node to display above the separator.
   */
  title: string;
  /**
   * The subtitle of the node to display below the separator.
   */
  subtitle?: string;
  /**
   * The body content to display.
   */
  body?: string;
}>();

const className = computed(
  () =>
    "cy-node-display " +
    (props.variant === GraphMode.tree
      ? "cy-node-tree q-pa-sm"
      : "cy-node-tim q-px-lg q-py-md")
);

const cardStyle = computed(() => `border-color: ${props.color};`);
const separatorStyle = computed(() => `background-color: ${props.color};`);
</script>
