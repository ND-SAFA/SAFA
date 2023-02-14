<template>
  <div v-if="isOpen">
    <artifact-body />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { appStore } from "@/hooks";
import { ArtifactBody } from "../display";

/**
 * Displays artifact content.
 */
export default defineComponent({
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
