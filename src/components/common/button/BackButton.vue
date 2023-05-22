<template>
  <text-button text icon="back" :label="buttonLabel" @click="handleClick" />
</template>

<script lang="ts">
/**
 * A generic back button
 */
export default {
  name: "BackButton",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import type { BackButtonProps } from "@/types";
import { getParams, navigateBack, navigateTo, Routes } from "@/router";
import TextButton from "./TextButton.vue";

const props = defineProps<BackButtonProps>();

const buttonLabel = computed(() => {
  if (props.toProject) {
    return "Back To Project";
  } else if (props.label) {
    return props.label;
  } else {
    return "Go Back";
  }
});

/**
 * Routes back to the given page.
 */
function handleClick(): void {
  if (props.toProject) {
    navigateTo(Routes.ARTIFACT, getParams());
  } else if (props.route) {
    navigateTo(props.route);
  } else {
    navigateBack();
  }
}
</script>
