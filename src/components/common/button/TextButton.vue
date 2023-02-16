<template>
  <v-btn
    :disabled="disabled"
    :size="buttonSize"
    :block="block"
    :loading="loading"
    :color="buttonColor"
    :value="value"
    :class="buttonClassName"
    :data-cy="dataCy"
    :variant="buttonVariant"
    @click="emit('click')"
  >
    <icon
      v-if="iconId || iconVariant"
      :id="iconId"
      :variant="iconVariant"
      class="mr-1"
    />
    <slot />
  </v-btn>
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
import { defineProps, defineEmits, computed } from "vue";
import { IconVariant } from "@/types";
import Icon from "@/components/common/display/icon/Icon.vue";

const props = defineProps<{
  outlined?: boolean;
  text?: boolean;
  disabled?: boolean;
  large?: boolean;
  small?: boolean;
  block?: boolean;
  loading?: boolean;
  color?: string;
  iconId?: string;
  iconVariant?: IconVariant;
  value?: string;
  y?: string;
  x?: string;
  classes?: string;
  variant?: "add" | "edit" | "save" | "delete" | "cancel" | "artifact";
  dataCy?: string;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const buttonColor = computed(() => {
  switch (props.variant) {
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
  let classNames = props.classes || "";

  if (props.x) classNames += ` mx-${props.x}`;
  if (props.y) classNames += ` my-${props.y}`;
  if (props.color) classNames += ` text-${props.color}`;

  return classNames;
});

const buttonVariant = computed(() => {
  if (props.outlined) {
    return "outlined";
  } else if (props.text) {
    return "text";
  } else {
    return "elevated";
  }
});

const buttonSize = computed(() => {
  if (props.large) {
    return "large";
  } else if (props.small) {
    return "small";
  } else {
    return undefined;
  }
});
</script>
