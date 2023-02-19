<template>
  <q-separator
    :class="className"
    :vertical="props.vertical"
    :inset="props.inset"
    :color="separatorColor"
  />
</template>

<script lang="ts">
/**
 * A generic component for drawing a line separator.
 */
export default {
  name: "Separator",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { SizeType } from "@/types";

const props = defineProps<{
  x?: SizeType;
  y?: SizeType;
  l?: SizeType;
  r?: SizeType;
  t?: SizeType;
  b?: SizeType;
  vertical?: boolean;
  class?: string;
  inset?: boolean;
  nav?: boolean;
  color?: string;
}>();

const convertMargin = (value: SizeType) => {
  switch (value) {
    case "":
      return "none";
    case "1":
      return "xs";
    case "2":
      return "sm";
    case "3":
      return "md";
    case "4":
      return "lg";
    case "5":
    default:
      return "xl";
  }
};

const className = computed(() => {
  let classNames = props.class || "";

  if (props.nav) classNames += ` faded`;
  if (props.x) classNames += ` q-mx-${convertMargin(props.x)}`;
  if (props.l) classNames += ` q-ml-${convertMargin(props.l)}`;
  if (props.r) classNames += ` q-mr-${convertMargin(props.r)}`;
  if (props.y) classNames += ` q-my-${convertMargin(props.y)}`;
  if (props.t) classNames += ` q-mt-${convertMargin(props.t)}`;
  if (props.b) classNames += ` q-mb-${convertMargin(props.b)}`;

  return classNames;
});

const separatorColor = computed(() => {
  if (props.color) {
    return props.color;
  } else if (props.nav) {
    return "accent";
  } else {
    return undefined;
  }
});
</script>
