<template>
  <img :src="iconLight" alt="SAFA" :class="className" @click="emit('click')" />
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
import iconLight from "@/assets/images/SAFA-primary.svg";

const props = defineProps<SafaIconProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

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
