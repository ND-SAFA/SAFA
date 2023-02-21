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
import { SizeType, ThemeColor } from "@/types";
import { useMargins } from "@/hooks";

const props = defineProps<{
  /**
   * Whether to render the separator vertically.
   */
  vertical?: boolean;
  /**
   * Whether to pad the separator.
   */
  inset?: boolean;
  /**
   * Whether to style to separator for the navigation bar.
   */
  nav?: boolean;
  /**
   * The color to render the component with.
   */
  color?: ThemeColor;
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
   * The classnames to include on this component.
   */
  class?: string;
}>();

const className = useMargins(props, [
  ["nav", "faded"],
  ["class", props.class],
]);

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
