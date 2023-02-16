<template>
  <v-icon :color="iconColor" :size="size" :style="iconStyle">
    {{ iconId }}
  </v-icon>
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
import { computed, defineProps } from "vue";
import { IconVariant } from "@/types";

const props = defineProps<{
  variant?: IconVariant;
  color?: "primary" | "secondary" | "error" | "accent" | string;
  id?: string;
  size?: "small" | "medium" | "large";
  rotate?: number;
  style?: string;
}>();

const iconId = computed(() => {
  if (props.id) {
    return props.id;
  }

  switch (props.variant) {
    case "add":
      return "mdi-plus";
    case "edit":
      return "mdi-pencil";
    case "save":
      return "mdi-content-save";
    case "saving":
      return "mdi-cloud-upload-outline";
    case "delete":
      return "mdi-delete";
    case "cancel":
      return "mdi-close";
    case "info":
      return "mdi-alert-circle-outline";
    case "error":
      return "mdi-alert-octagon-outline";
    case "success":
      return "mdi-check-outline";
    case "artifact":
      return "mdi-application-array-outline";
    case "trace":
      return "mdi-ray-start-arrow";
    case "upload":
      return "mdi-folder-arrow-up-outline";
    case "integrate":
      return "mdi-transit-connection-variant";
    case "warning":
      return "mdi-hazard-lights";
    case "back":
      return "mdi-arrow-left";
    case "account":
      return "mdi-account-circle";
    case "search":
      return "mdi-magnify";
    case "notification":
      return "mdi-bell-outline";
    case "home-list":
      return "mdi-view-list";
    case "home-add":
      return "mdi-folder-plus-outline";
    case "job-complete":
      return "mdi-check-circle-outline";
    case "job-cancel":
      return "mdi-close-circle-outline";
    default:
      return "";
  }
});

const iconColor = computed(() => {
  if (props.color) {
    return props.color;
  }

  switch (props.variant) {
    case "home-list":
    case "home-add":
      return "primary";
    case "warning":
      return "secondary";
    case "error":
      return "error";
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
