<template>
  <img
    v-if="!darkMode"
    :src="iconLight"
    alt="SAFA"
    class="full-width"
    @click="$emit('click')"
  />
  <img
    v-else
    :src="iconDark"
    alt="SAFA"
    class="full-width"
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
import { defineEmits, computed } from "vue";
import { useTheme } from "vuetify";
import iconLight from "@/assets/images/SAFA-primary.svg";
import iconDark from "@/assets/images/SAFA-secondary.svg";

defineEmits<{
  (e: "click"): void;
}>();

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);
</script>
