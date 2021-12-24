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

/**
 * Loading bar used in application header.
 */
export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      required: true,
    },
  },
});
</script>
