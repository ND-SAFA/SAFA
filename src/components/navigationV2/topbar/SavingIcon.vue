<template>
  <v-tooltip bottom z-index="10000" v-if="isSaving">
    <template v-slot:activator="{ on, attrs }">
      <v-progress-circular
        v-on="on"
        v-bind="attrs"
        indeterminate
        size="36"
        color="accent"
      >
        <v-icon color="accent"> mdi-cloud-upload-outline </v-icon>
      </v-progress-circular>
    </template>
    <span>Saving...</span>
  </v-tooltip>
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
