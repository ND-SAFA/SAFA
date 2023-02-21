<template>
  <q-btn
    :disable="props.disabled"
    :size="buttonSize"
    :outline="props.outlined"
    :flat="props.text"
    :loading="props.loading"
    :percentage="props.percentage"
    :color="buttonColor"
    :class="buttonClassName"
    :data-cy="props.dataCy"
    @click="emit('click')"
  >
    <icon v-if="props.icon" :variant="props.icon" class="q-mr-sm" />
    <typography
      v-if="!!props.label"
      :value="props.label"
      :small="props.small"
      :large="props.large"
    />
    <slot />
  </q-btn>
</template>

<script lang="ts">
/**
 * A generic text button.
 */
export default {
  name: "TextButton",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { IconVariant, SizeType, ThemeColor } from "@/types";
import { useMargins } from "@/hooks";
import Icon from "@/components/common/display/icon/Icon.vue";
import Typography from "@/components/common/display/Typography.vue";

const props = defineProps<{
  /**
   * Renders an outlined button.
   */
  outlined?: boolean;
  /**
   * Renders a flat text button.
   */
  text?: boolean;
  /**
   * Renders the button as a full width block.
   */
  block?: boolean;
  /**
   * The loading percentage to render on a loading button.
   */
  percentage?: number;
  /**
   * The button text to display, if not using the default slot.
   */
  label?: string;
  /**
   * Whether the component is disabled.
   */
  disabled?: boolean;
  /**
   * Renders a smaller component.
   */
  small?: boolean;
  /**
   * Renders a larger component.
   */
  large?: boolean;
  /**
   * Whether the component is loading.
   */
  loading?: string;
  /**
   * The color to render the component with.
   */
  color?: ThemeColor;
  /**
   * The type of icon to render.
   */
  icon?: IconVariant;
  /**
   * The classnames to include on this component.
   */
  class?: string;
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
   * The testing selector to set.
   */
  dataCy?: string;
}>();

const emit = defineEmits<{
  /**
   * Called when clicked.
   */
  (e: "click"): void;
}>();

const buttonClassName = useMargins(props, [
  ["color", `text-${props.color}`],
  ["block", "full-width"],
  ["class", props.class],
]);

const buttonColor = computed(() => {
  switch (props.icon) {
    case "add":
    case "save":
      return "primary";
    case "delete":
      return "negative";
    default:
      return props.color;
  }
});

const buttonSize = computed(() => {
  if (props.large) {
    return "lg";
  } else if (props.small) {
    return "sm";
  } else {
    return undefined;
  }
});
</script>
