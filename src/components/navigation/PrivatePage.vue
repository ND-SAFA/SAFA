<template>
  <v-container :class="fullWindow ? 'full-window-page' : ''">
    <slot name="page" />
    <app-bar />
    <left-nav-drawer />
    <right-nav-drawer />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { LeftNavDrawer, RightNavDrawer } from "./side-panels";
import AppBar from "./AppBar.vue";

/**
 * Displays a page with top and side bars.
 */
export default Vue.extend({
  name: "PrivatePage",
  components: {
    AppBar,
    LeftNavDrawer,
    RightNavDrawer,
  },
  props: {
    fullWindow: Boolean,
  },
});
</script>
