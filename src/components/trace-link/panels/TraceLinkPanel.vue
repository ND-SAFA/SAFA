<template>
  <div v-if="isOpen" data-cy="panel-trace-display">
    <trace-link-buttons />
    <trace-link-content />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { TraceLinkButtons, TraceLinkContent } from "../base";

/**
 * Displays trace link information.
 */
export default Vue.extend({
  name: "TraceLinkPanel",
  components: { TraceLinkButtons, TraceLinkContent },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayTrace";
    },
  },
});
</script>
