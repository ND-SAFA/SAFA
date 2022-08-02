<template>
  <v-container :class="fullWindow ? 'full-window-page' : ''">
    <slot name="page" />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays a page with top and side bars.
 */
export default Vue.extend({
  name: "PrivatePage",
  props: {
    fullWindow: Boolean,
  },
});
</script>
