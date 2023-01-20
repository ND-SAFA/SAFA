<template>
  <div v-if="isOpen"></div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Displays artifact level information.
 */
export default Vue.extend({
  name: "ArtifactLevelPanel",
  components: {},
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayArtifactLevel";
    },
  },
});
</script>
