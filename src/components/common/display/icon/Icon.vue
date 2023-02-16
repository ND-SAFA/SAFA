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
      // "mdi-alpha-a-box-outline"
      return "mdi-application-array-outline";
    case "trace":
      return "mdi-ray-start-arrow";
    case "upload":
      return "mdi-folder-arrow-up-outline";
    case "download":
      return "mdi-download";
    case "sync":
      return "mdi-cloud-sync-outline";
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
    case "share":
      return "mdi-share-variant";
    case "logs":
      return "mdi-post-outline";
    case "more":
      return "mdi-dots-horizontal";
    case "undo":
      return "mdi-undo";
    case "redo":
      return "mdi-redo";
    case "home-list":
      return "mdi-view-list";
    case "home-add":
      return "mdi-folder-plus-outline";
    case "job-complete":
      return "mdi-check-circle-outline";
    case "job-cancel":
      return "mdi-close-circle-outline";
    case "trace-approve":
      return "mdi-check-circle-outline";
    case "trace-decline":
      return "mdi-close-circle-outline";
    case "trace-decline-all":
      return "mdi-close-circle-multiple-outline";
    case "trace-unreview":
      return "mdi-checkbox-blank-circle-outline";
    case "view-tim":
      return "mdi-ballot";
    case "view-tree":
      return "mdi-family-tree";
    case "view-table":
      return "mdi-table-multiple";
    case "view-delta":
      return "mdi-compare";
    case "graph-zoom-in":
      return "mdi-magnify-plus-outline";
    case "graph-zoom-out":
      return "mdi-magnify-minus-outline";
    case "graph-center":
      return "mdi-graphql";
    case "graph-refresh":
      return "mdi-refresh";
    case "nav-toggle":
      return "mdi-menu-open";
    case "nav-home":
      return "mdi-home";
    case "nav-create":
      return "mdi-folder-plus";
    case "nav-open":
      return "mdi-list-box";
    case "nav-uploads":
      return "mdi-folder-upload";
    case "nav-artifact":
      return "mdi-family-tree";
    case "nav-trace":
      return "mdi-link-box";
    case "nav-settings":
      return "mdi-cog-box";
    case "group-open":
      return "mdi-chevron-up";
    case "group-open-all":
      return "mdi-arrow-expand-all";
    case "group-close":
      return "mdi-chevron-down";
    case "group-close-all":
      return "mdi-arrow-collapse-all";
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
    case "trace-approve":
      return "primary";
    case "warning":
      return "secondary";
    case "error":
    case "trace-decline":
    case "trace-decline-all":
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
