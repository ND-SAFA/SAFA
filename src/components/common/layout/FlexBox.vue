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
import { computed, withDefaults } from "vue";
import { AlignType, JustifyType, SizeType } from "@/types";
import { useMargins } from "@/hooks";

const props = withDefaults(
  defineProps<{
    /**
     * How to align the content.
     */
    align?: AlignType;
    /**
     * How to justify the content.
     */
    justify?: JustifyType;
    /**
     * The max width to set (in pixels)
     */
    maxWidth?: number;
    /**
     * Whether to expand to full width.
     */
    fullWidth?: boolean;
    /**
     * Whether to render as a flex column instead of row.
     */
    column?: boolean;
    /**
     * Whether to allow the items to wrap.
     * @default Unset unless an explicit boolean true or false is set.
     */
    wrap?: boolean;
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

const className = useMargins(props, () => [
  [true, props.column ? "column" : "row"],
  ["align", `align-${props.align}`],
  ["justify", `justify-${props.justify}`],
  ["fullWidth", "full-width"],
  ["wrap", "wrap"],
  [props.wrap === false, "nowrap"],
]);

const style = computed(() =>
  props.maxWidth ? `max-width: ${props.maxWidth}px` : ""
);
</script>
