<template>
  <div :class="className" :style="style">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * A generic component for displaying flex content.
 */
export default {
  name: "FlexBox",
};
</script>

<script setup lang="ts">
import { computed, withDefaults, defineProps } from "vue";
import { JustifyType, SizeType, AlignType } from "@/types";

const props = withDefaults(
  defineProps<{
    align?: AlignType;
    justify?: JustifyType;
    x?: SizeType;
    y?: SizeType;
    l?: SizeType;
    r?: SizeType;
    t?: SizeType;
    b?: SizeType;
    maxWidth?: number;
    fullWidth?: boolean;
    column?: boolean;
    wrap?: boolean;
  }>(),
  {
    align: "start",
    justify: "start",
    x: "",
    y: "",
    l: "",
    r: "",
    t: "",
    b: "",
    maxWidth: undefined,
  }
);

const style = computed(() =>
  props.maxWidth ? `max-width: ${props.maxWidth}px` : ""
);

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
  let classNames = `flex `;

  if (props.align) classNames += ` align-${props.align}`;
  if (props.justify) classNames += ` justify-${props.justify}`;
  if (props.fullWidth) classNames += ` fill-width`;
  if (props.column) classNames += ` column`;
  if (props.wrap) classNames += ` wrap`;
  if (props.wrap === false) classNames += ` nowrap`;
  if (props.x) classNames += ` q-mx-${convertMargin(props.x)}`;
  if (props.l) classNames += ` q-ml-${convertMargin(props.l)}`;
  if (props.r) classNames += ` q-mr-${convertMargin(props.r)}`;
  if (props.y) classNames += ` q-my-${convertMargin(props.y)}`;
  if (props.t) classNames += ` q-mt-${convertMargin(props.t)}`;
  if (props.b) classNames += ` q-mb-${convertMargin(props.b)}`;

  return classNames;
});
</script>
