<template>
  <img
    v-if="!darkMode"
    :src="iconLight"
    alt="SAFA"
    :class="className"
    @click="$emit('click')"
  />
  <img
    v-else
    :src="iconDark"
    alt="SAFA"
    :class="className"
    @click="$emit('click')"
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
import { useTheme } from "@/hooks";
import iconLight from "@/assets/images/SAFA-primary.svg";
import iconDark from "@/assets/images/SAFA-secondary.svg";

const props = defineProps<{
  /**
   * Whether the icon is clickable.
   */
  clickable?: boolean;
}>();

defineEmits<{
  (e: "click"): void;
}>();

const { darkMode } = useTheme();

const className = computed(() =>
  props.clickable ? "full-width clickable" : "full-width"
);
</script>
