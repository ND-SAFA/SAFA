<template>
  <div>
    <text-button text y="2" variant="artifact" @click="handleViewArtifact">
      View Artifact
    </text-button>
    <typography
      :variant="isCodeDisplay ? 'code' : 'body'"
      el="p"
      :value="selectedArtifactBody"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore, selectionStore } from "@/hooks";
import { Typography, TextButton } from "@/components/common";

/**
 * Displays the selected node's body.
 */
export default Vue.extend({
  name: "ArtifactBody",
  components: {
    TextButton,
    Typography,
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    artifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's body.
     */
    selectedArtifactBody(): string {
      return this.artifact?.body.trim() || "";
    },
    /**
     * An incredibly crude and temporary way to distinguish code nodes.
     *
     * @return Whether to display this body as code.
     */
    isCodeDisplay(): boolean {
      return this.artifact?.type.includes("code") || false;
    },
  },
  methods: {
    /**
     * Displays the entire artifact.
     */
    handleViewArtifact(): void {
      appStore.openDetailsPanel("displayArtifact");
    },
  },
});
</script>
