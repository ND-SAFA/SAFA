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
    <icon
      v-if="props.icon"
      :variant="props.icon"
      :class="!props.hideLabel ? 'q-mr-sm' : ''"
      :rotate="props.iconRotate"
    />
    <typography
      v-if="!!props.label && !props.hideLabel"
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
import type { TextButtonProps } from "@/types";
import { useMargins } from "@/hooks";
import { Icon, Typography } from "@/components/common/display";

const props = defineProps<TextButtonProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const buttonClassName = useMargins(props, () => [
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
