<template>
  <div :class="className">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * A generic flex box child.
 */
export default {
  name: "FlexItem",
};
</script>

<script setup lang="ts">
import { SizeType } from "@/types";
import { useMargins } from "@/hooks";

const props = defineProps<{
  /**
   * The x margin.
   */
  x?: SizeType;
  /**
   * The y margin.
   */
  y?: SizeType;
  /**
   * The left margin.
   */
  l?: SizeType;
  /**
   * The right margin.
   */
  r?: SizeType;
  /**
   * The top margin.
   */
  t?: SizeType;
  /**
   * The bottom margin.
   */
  b?: SizeType;
  /**
   * How many parts this column should take up, out of 12.
   */
  parts?: SizeType | "auto";
}>();

const className = useMargins(props, () => [["parts", `col-${props.parts}`]]);
</script>
