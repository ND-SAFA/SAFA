<template>
  <q-card flat bordered :class="className" :style="cardStyle">
    <div v-if="props.title" class="cy-node-title" data-cy="tree-node-type">
      <typography variant="subtitle" :value="props.title" bold />
    </div>

    <separator
      v-if="props.separator"
      :style="separatorStyle"
      :class="separatorClassName"
    />

    <div
      v-if="!!props.subtitle"
      class="cy-node-subtitle"
      data-cy="tree-node-name"
    >
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
import { ThemeColor } from "@/types";
import { Separator, Typography } from "@/components/common";

const props = defineProps<{
  /**
   * The type of node to display.
   */
  variant: "tim" | "artifact" | "footer";
  /**
   * The color of the node to display.
   */
  color: ThemeColor | string;
  /**
   * The title of the node to display above the separator.
   */
  title?: string;
  /**
   * The subtitle of the node to display below the separator.
   */
  subtitle?: string;
  /**
   * Whether to display a separator between the title and subtitle.
   */
  separator?: boolean;
  /**
   * The body content to display.
   */
  body?: string;
}>();

const className = computed(
  () =>
    "cy-node-display " +
    (props.color.includes("#") ? "" : `bd-${props.color} `) +
    {
      tim: "cy-node-tim q-px-lg q-py-md",
      artifact: "cy-node-artifact q-pa-sm",
      footer: "cy-node-footer q-pa-xs",
    }[props.variant]
);

const separatorClassName = computed(
  () =>
    "cy-node-separator " +
    (props.color.includes("#") ? "" : `bg-${props.color} `) +
    (props.variant !== "tim" ? "q-my-xs" : "q-my-sm")
);

const cardStyle = computed(() =>
  props.color.includes("#") ? `border-color: ${props.color};` : undefined
);
const separatorStyle = computed(() =>
  props.color.includes("#") ? `background-color: ${props.color};` : undefined
);
</script>
