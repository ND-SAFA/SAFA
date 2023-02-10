<template>
  <v-container v-if="sessionStore.doesSessionExist" :class="className">
    <slot />
  </v-container>
  <v-container v-else class="my-8">
    <div class="mx-auto width-fit" style="margin-top: 40vh">
      <v-progress-circular size="60" indeterminate />
    </div>
  </v-container>
</template>

<script lang="ts">
/**
 * Displays a page with top and sidebars.
 */
export default {
  name: "PrivatePage",
};
</script>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import { sessionStore } from "@/hooks";

const props = defineProps<{
  fullWindow?: boolean;
}>();

const className = computed(() =>
  props.fullWindow ? "full-window-page primary-bg" : "primary-bg"
);
</script>
