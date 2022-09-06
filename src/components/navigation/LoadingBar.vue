<template>
  <v-progress-linear
    rounded
    height="5"
    v-show="isLoading"
    indeterminate
    absolute
    bottom
    color="secondary"
    data-cy="app-loading"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Loading bar used in application header.
 */
export default Vue.extend({
  name: "LoadingBar",
  computed: {
    /**
     * @return Whether the app is loading
     */
    isLoading(): boolean {
      return appStore.isLoading > 0;
    },
  },
});
</script>
