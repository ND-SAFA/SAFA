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
import { FlexBoxProps } from "@/types";
import { useMargins } from "@/hooks";

const props = withDefaults(defineProps<FlexBoxProps>(), {
  align: "start",
  justify: "start",
  x: "",
  y: "",
  l: "",
  r: "",
  t: "",
  b: "",
  maxWidth: undefined,
});

const className = useMargins(props, () => [
  [true, props.column ? "column" : "row"],
  ["align", `align-${props.align}`],
  ["justify", `justify-${props.justify}`],
  ["fullWidth", "full-width"],
  ["wrap", "wrap"],
  [!props.wrap, "nowrap"],
]);

const style = computed(() =>
  props.maxWidth ? `max-width: ${props.maxWidth}px` : ""
);
</script>
