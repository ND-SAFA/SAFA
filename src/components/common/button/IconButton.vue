<template>
  <q-btn
    :color="props.color"
    :fab="props.fab"
    :class="props.disabled ? 'disable-events' : ''"
    :size="size"
    :data-cy="props.dataCy"
    :flat="!props.fab"
    :round="!props.fab"
    @click="emit('click')"
  >
    <icon :variant="props.icon" :rotate="props.rotate" />
    <q-tooltip :delay="200">
      {{ tooltip }}
    </q-tooltip>
  </q-btn>
</template>

<script lang="ts">
/**
 * A generic icon button.
 */
export default {
  name: "IconButton",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { IconVariant, ThemeColor } from "@/types";
import Icon from "@/components/common/display/icon/Icon.vue";

const props = defineProps<{
  /**
   * The type of icon to render.
   */
  icon?: IconVariant;
  /**
   * The tooltip message to display on this button.
   */
  tooltip: string;
  /**
   * Whether to render this button as a fab.
   */
  fab?: boolean;
  /**
   * Rotates the icon on this button (in degrees).
   */
  rotate?: number;
  /**
   * The color to render the component with.
   */
  color?: ThemeColor;
  /**
   * Whether the component is disabled.
   */
  disabled?: string;
  /**
   * Renders a smaller component.
   */
  small?: boolean;
  /**
   * Renders a larger component.
   */
  large?: boolean;
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

const size = computed(() => {
  if (props.small) {
    return "sm";
  } else if (props.large) {
    return "lg";
  } else {
    return "";
  }
});
</script>
