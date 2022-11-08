<template>
  <div>
    <v-btn class="my-2" text @click="handleViewArtifact">
      <v-icon class="mr-1">mdi-application-array-outline</v-icon>
      View Artifact
    </v-btn>
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
import { Typography } from "@/components/common";

/**
 * Displays the selected node's body..
 */
export default Vue.extend({
  name: "ArtifactBody",
  components: {
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
