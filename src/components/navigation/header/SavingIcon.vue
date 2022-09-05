<template>
  <v-chip outlined small label color="secondary" v-if="isSaving">
    <v-progress-circular indeterminate class="mr-2" size="16" />
    Saving
  </v-chip>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Renders app saving state.
 */
export default Vue.extend({
  name: "SavingIcon",
  computed: {
    isSaving(): boolean {
      return appStore.isSaving;
    },
  },
});
</script>
