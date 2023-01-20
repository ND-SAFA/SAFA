<template>
  <div v-if="isOpen"></div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Displays trace matrix information.
 */
export default Vue.extend({
  name: "TraceMatrixPanel",
  components: {},
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayTraceMatrix";
    },
  },
});
</script>
