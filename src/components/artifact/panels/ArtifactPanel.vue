<template>
  <div v-if="isOpen">
    <artifact-buttons />
    <artifact-content />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { appStore } from "@/hooks";
import { ArtifactButtons, ArtifactContent } from "../display";

/**
 * Displays artifact information.
 */
export default defineComponent({
  name: "ArtifactPanel",
  components: { ArtifactContent, ArtifactButtons },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayArtifact";
    },
  },
});
</script>
