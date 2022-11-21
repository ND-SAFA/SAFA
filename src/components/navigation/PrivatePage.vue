<template>
  <v-container v-if="isLoggedIn" :class="fullWindow ? 'full-window-page' : ''">
    <slot name="page" />
  </v-container>
  <v-container v-else class="my-8">
    <div class="mx-auto width-fit" style="margin-top: 40vh">
      <v-progress-circular size="60" indeterminate />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { sessionStore } from "@/hooks";

/**
 * Displays a page with top and sidebars.
 */
export default Vue.extend({
  name: "PrivatePage",
  props: {
    fullWindow: Boolean,
  },
  computed: {
    /**
     * Returns whether a user is currently logged in.
     */
    isLoggedIn() {
      return sessionStore.doesSessionExist;
    },
  },
});
</script>
