<template>
  <div v-if="isOpen">
    <artifact-body />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { ArtifactBody } from "../base";

/**
 * Displays artifact content.
 */
export default Vue.extend({
  name: "ArtifactBodyPanel",
  components: { ArtifactBody },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayArtifactBody";
    },
  },
});
</script>
