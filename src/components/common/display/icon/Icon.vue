<template>
  <v-icon :color="iconColor" :size="size">{{ iconId }}</v-icon>
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
  color?: "primary" | "secondary" | string;
  id?: string;
  size?: "small" | "medium" | "large";
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
    default:
      return "";
  }
});
</script>
