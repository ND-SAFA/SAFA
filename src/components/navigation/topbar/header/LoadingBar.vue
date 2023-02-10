<template>
  <v-progress-linear
    v-show="appStore.isLoading > 0"
    rounded
    height="5"
    indeterminate
    absolute
    bottom
    color="secondary"
    data-cy="app-loading"
  />
</template>

<script lang="ts">
/**
 * Loading bar used in application header.
 */
export default {
  name: "LoadingBar",
};
</script>

<script setup lang="ts">
import { appStore } from "@/hooks";
</script>
