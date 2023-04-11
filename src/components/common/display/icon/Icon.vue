<template>
  <q-icon
    :color="iconColor"
    :size="props.size"
    :style="iconStyle"
    :name="iconId"
  />
</template>

<script lang="ts">
/**
 * Icon
 */
export default {
  name: "Icon",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { IconVariant, ThemeColor } from "@/types";
import { getIcon } from "@/util";

const props = defineProps<{
  /**
   * The icon variant to render.
   */
  variant?: IconVariant;
  /**
   * The id of an icon, if not rendering a preset variant.
   */
  id?: string;
  /**
   * The size of the icon.
   */
  size?: "sm" | "md" | "lg";
  /**
   * How much to rotate the icon (in degrees).
   */
  rotate?: number;
  /**
   * The color to render the component with.
   */
  color?: ThemeColor;
  /**
   * The  style to include on the component.
   */
  style?: string;
}>();

const iconId = computed(() => {
  if (props.id) {
    return props.id;
  }

  return getIcon(props.variant);
});

const iconColor = computed(() => {
  if (props.color) {
    return props.color;
  }

  switch (props.variant) {
    case "home-list":
    case "home-add":
    case "trace-approve":
      return "primary";
    case "warning":
      return "secondary";
    case "error":
    case "trace-decline":
    case "trace-decline-all":
      return "negative";
    default:
      return "";
  }
});

const iconStyle = computed(() => {
  if (props.style) {
    return props.style;
  } else if (props.rotate) {
    return `transform: rotate(${props.rotate}deg)`;
  } else {
    return "";
  }
});
</script>
