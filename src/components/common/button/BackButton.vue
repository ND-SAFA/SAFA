<template>
  <v-btn text @click="handleClick">
    <v-icon left> mdi-arrow-left </v-icon>
    {{ text }}
  </v-btn>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { getParams, navigateBack, navigateTo, Routes } from "@/router";

/**
 * A generic back button
 */
export default defineComponent({
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
    toProject: Boolean,
  },
  methods: {
    /**
     * Routes back to the given page.
     */
    handleClick(): void {
      if (this.toProject) {
        navigateTo(Routes.ARTIFACT, getParams());
      } else if (this.route) {
        navigateTo(this.route);
      } else {
        navigateBack();
      }
    },
  },
});
</script>

<style scoped></style>
