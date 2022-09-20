<template>
  <img
    :src="pathToLogo"
    alt="SAFA"
    class="full-width"
    @click="$emit('click')"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

/**
 * Displays the SAFA icon.
 */
export default Vue.extend({
  name: "SafaIcon",
  props: {
    variant: String as PropType<"primary" | "secondary">,
  },
  data() {
    return {
      pathToLogo:
        this.variant === "primary"
          ? require("@/assets/SAFA-primary.svg")
          : require("@/assets/SAFA-secondary.svg"),
    };
  },
});
</script>
