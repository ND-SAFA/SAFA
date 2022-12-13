<template>
  <img
    :src="pathToLogo"
    alt="SAFA"
    class="full-width"
    @click="$emit('click')"
  />
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays the SAFA icon.
 */
export default Vue.extend({
  name: "SafaIcon",
  data() {
    return {
      pathToLogo: this.$vuetify.theme.dark
        ? require("@/assets/SAFA-secondary.svg")
        : require("@/assets/SAFA-primary.svg"),
    };
  },
});
</script>
