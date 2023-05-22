<template>
  <img
    v-if="!darkMode"
    :src="iconLight"
    alt="SAFA"
    :class="className"
    @click="emit('click')"
  />
  <img
    v-else
    :src="iconDark"
    alt="SAFA"
    :class="className"
    @click="emit('click')"
  />
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
import { useTheme } from "@/hooks";
import iconLight from "@/assets/images/SAFA-primary.svg";
import iconDark from "@/assets/images/SAFA-secondary.svg";

const props = defineProps<SafaIconProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const { darkMode } = useTheme();

const className = computed(() => {
  let classNames = "icon-safa full-width";

  if (props.clickable) {
    classNames += " clickable";
  }
  if (!props.hidden) {
    classNames += " visible";
  }

  return classNames;
});
</script>
