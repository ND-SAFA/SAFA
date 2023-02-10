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

const className = computed(() => {
  let classNames = `d-flex `;

  if (props.align) classNames += ` align-${props.align}`;
  if (props.justify) classNames += ` justify-${props.justify}`;
  if (props.fullWidth) classNames += ` full-width`;
  if (props.column) classNames += ` flex-column`;
  if (props.wrap) classNames += ` flex-wrap`;
  if (props.x) classNames += ` mx-${props.x}`;
  if (props.l) classNames += ` ml-${props.l}`;
  if (props.r) classNames += ` mr-${props.r}`;
  if (props.y) classNames += ` my-${props.y}`;
  if (props.t) classNames += ` mt-${props.t}`;
  if (props.b) classNames += ` mb-${props.b}`;

  return classNames;
});
</script>
