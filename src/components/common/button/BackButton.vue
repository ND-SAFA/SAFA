<template>
  <v-btn text @click="handleClick">
    <v-icon left> mdi-arrow-left </v-icon>
    {{ text }}
  </v-btn>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { navigateBack, navigateTo, Routes } from "@/router";

/**
 * A generic back button
 */
export default Vue.extend({
  name: "BackButton",
  props: {
    text: {
      type: String,
      default: "Go Back",
    },
    route: {
      type: String as PropType<Routes | undefined>,
      default: undefined,
    },
  },
  methods: {
    /**
     * Routes back to the given page.
     */
    handleClick(): void {
      if (this.route) {
        navigateTo(this.route);
      } else {
        navigateBack();
      }
    },
  },
});
</script>

<style scoped></style>
