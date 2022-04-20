<template>
  <v-progress-linear
    rounded
    height="5"
    v-show="isLoading"
    indeterminate
    absolute
    bottom
    color="secondary"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { appModule } from "@/store";

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
      return appModule.getIsLoading;
    },
  },
});
</script>
