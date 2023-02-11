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
    @click.native="emit('click')"
  >
    <v-icon v-if="buttonIconId" class="mr-1">{{ buttonIconId }}</v-icon>
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

const buttonIconId = computed(() => {
  switch (props.variant) {
    case "add":
      return "mdi-plus";
    case "edit":
      return "mdi-pencil";
    case "save":
      return "mdi-content-save";
    case "delete":
      return "mdi-delete";
    case "cancel":
      return "mdi-close";
    case "artifact":
      return "mdi-application-array-outline";
    default:
      return props.iconId;
  }
});

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
