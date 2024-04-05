<template>
  <q-card
    flat
    bordered
    :class="className"
    :style="cardStyle"
    @mousedown="mouseDownTime = new Date().getTime()"
    @mouseup="mouseUpTime = new Date().getTime()"
    @click="handleClick"
    @touchend="handleClick"
  >
    <flex-box
      v-if="props.title"
      class="cy-node-title"
      justify="center"
      align="center"
      data-cy="tree-node-type"
    >
      <icon :id="iconId" :color="iconColor" size="sm" />
      <typography
        variant="subtitle"
        :value="props.title"
        bold
        l="1"
        align="center"
        ellipsis
        color="text"
      />
    </flex-box>

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
import { computed, ref } from "vue";
import { NodeDisplayProps } from "@/types";
import { timStore } from "@/hooks";
import { Separator, Typography, Icon, FlexBox } from "@/components/common";

const props = defineProps<NodeDisplayProps>();

const emit = defineEmits<{
  (event: "click"): void;
}>();

const mouseDownTime = ref(0);
const mouseUpTime = ref(0);

const className = computed(
  () =>
    "cy-node-display " +
    (props.selected ? "cy-node-selected " : "") +
    (props.color.includes("#") ? "" : `bd-${props.color} `) +
    {
      tim: "cy-node-tim q-px-lg q-py-md",
      artifact: "cy-node-artifact q-pa-sm",
      footer: "cy-node-footer q-pa-xs",
      sidebar: "cy-node-sidebar q-pa-xs",
      menu: "cy-node-menu q-pa-xs",
    }[props.variant]
);

const separatorClassName = computed(
  () =>
    "cy-node-separator " +
    (props.color.includes("#") ? "" : `bg-${props.color} `) +
    (props.variant !== "tim" ? "q-mt-xs q-mb-none" : "q-my-sm")
);

const cardStyle = computed(() =>
  props.color.includes("#") ? `border-color: ${props.color};` : undefined
);
const separatorStyle = computed(() =>
  props.color.includes("#") ? `background-color: ${props.color};` : undefined
);

const iconId = computed(() =>
  props.title ? timStore.getTypeIcon(props.title) : undefined
);

const iconColor = computed(() =>
  props.title ? timStore.getTypeColor(props.title) : undefined
);

/**
 * Handles a click event, as long as it isn't a drag event.
 */
function handleClick(): void {
  if (mouseUpTime.value - mouseDownTime.value > 200) return;

  emit("click");
}
</script>
