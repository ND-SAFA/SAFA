<template>
  <svg
    id="logo-safa"
    xmlns="http://www.w3.org/2000/svg"
    width="100%"
    height="80pt"
    :viewBox="viewBox"
    preserveAspectRatio="xMidYMid meet"
    :class="className"
    @click="emit('click')"
  >
    <defs>
      <linearGradient
        id="color-gradient"
        x1="5%"
        :x2="props.iconOnly ? '100%' : '40%'"
        y1="0"
        y2="0"
        gradientUnits="userSpaceOnUse"
      >
        <stop offset="0%" :stop-color="Colors.gradient1" />
        <stop offset="100%" :stop-color="Colors.greenDark" />
      </linearGradient>
      <linearGradient
        id="color-gradient-full"
        x1="0%"
        x2="8%"
        y1="0"
        y2="0"
        gradientUnits="userSpaceOnUse"
      >
        <stop offset="0%" :stop-color="Colors.gradient1" />
        <stop offset="50%" :stop-color="Colors.gradient5" />
        <stop offset="100%" :stop-color="Colors.gradient9" />
      </linearGradient>
    </defs>
    <safa-logo />
    <safa-name v-if="!props.iconOnly" />
  </svg>
</template>

<script lang="ts">
/**
 * Displays the SAFA icon.
 */
export default {
  name: "SafaIcon",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { SafaIconProps } from "@/types";
import { Colors } from "@/util";
import SafaName from "./SafaName.vue";
import SafaLogo from "./SafaLogo.vue";

const props = defineProps<SafaIconProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const className = computed(() => {
  let classNames = "icon-safa";

  if (props.clickable) {
    classNames += " clickable";
  }
  if (!props.hidden) {
    classNames += " visible";
  }
  if (props.iconOnly) {
    classNames += " logo";
  }

  return classNames;
});

const viewBox = computed(() => {
  if (props.iconOnly) {
    return "0 0 620 500";
  } else {
    return "0 0 1750 480";
  }
});
</script>
