<template>
  <text-button text icon-variant="back" @click="handleClick">
    {{ text }}
  </text-button>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { getParams, navigateBack, navigateTo, Routes } from "@/router";
import TextButton from "@/components/common/button/TextButton.vue";

/**
 * A generic back button
 */
export default defineComponent({
  name: "BackButton",
  components: { TextButton },
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
