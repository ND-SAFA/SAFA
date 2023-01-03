<template>
  <div>
    <text-button text y="2" variant="artifact" @click="handleViewArtifact">
      View Artifact
    </text-button>
    <panel-card class="pb-4">
      <typography default-expanded :variant="variant" el="p" :value="body" />
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ReservedArtifactType, TextType } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { Typography, TextButton, PanelCard } from "@/components/common";

/**
 * Displays the selected node's body.
 */
export default Vue.extend({
  name: "ArtifactBody",
  components: {
    TextButton,
    Typography,
    PanelCard,
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
    body(): string {
      return this.artifact?.body.trim() || "";
    },
    /**
     * @return The selected artifact's body text variant.
     */
    variant(): TextType {
      return this.artifact?.type === ReservedArtifactType.github
        ? "code"
        : "expandable";
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
