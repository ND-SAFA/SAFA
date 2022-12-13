<template>
  <img
    v-if="!this.$vuetify.theme.dark"
    src="@/assets/SAFA-primary.svg"
    alt="SAFA"
    class="full-width"
    @click="$emit('click')"
  />
  <img
    v-else
    src="@/assets/SAFA-secondary.svg"
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
});
</script>
