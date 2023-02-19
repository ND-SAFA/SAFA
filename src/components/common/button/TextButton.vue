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
import { IconVariant } from "@/types";
import Icon from "@/components/common/display/icon/Icon.vue";
import Typography from "@/components/common/display/Typography.vue";

const props = defineProps<{
  outlined?: boolean;
  text?: boolean;
  disabled?: boolean;
  large?: boolean;
  small?: boolean;
  block?: boolean;
  loading?: boolean;
  percentage?: number;
  color?: string;
  y?: string;
  x?: string;
  class?: string;
  icon?: IconVariant;
  label?: string;
  dataCy?: string;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const buttonColor = computed(() => {
  switch (props.icon) {
    case "add":
    case "save":
      return "primary";
    case "delete":
      return "error";
    default:
      return props.color;
  }
});

const buttonClassName = computed(() => {
  let classNames = props.class || "";

  if (props.x) classNames += ` mx-${props.x}`;
  if (props.y) classNames += ` my-${props.y}`;
  if (props.color) classNames += ` text-${props.color}`;
  if (props.block) classNames += ` full-width`;

  return classNames;
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
