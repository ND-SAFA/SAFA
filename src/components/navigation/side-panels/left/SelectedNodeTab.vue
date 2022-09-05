<template>
  <v-container class="mb-10">
    <div v-if="selectedArtifact !== undefined">
      <artifact-title />
      <artifact-traces />
      <artifact-documents />
      <artifact-errors />
    </div>

    <typography v-else align="center" el="p" value="No artifact is selected." />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { selectionStore } from "@/hooks";
import { Typography } from "@/components/common";
import ArtifactTitle from "./ArtifactTitle.vue";
import ArtifactTraces from "./ArtifactTraces.vue";
import ArtifactDocuments from "./ArtifactDocuments.vue";
import ArtifactErrors from "./ArtifactErrors.vue";

/**
 * Displays the selected node tab.
 */
export default Vue.extend({
  name: "SelectedNodeTab",
  components: {
    ArtifactErrors,
    ArtifactDocuments,
    ArtifactTraces,
    ArtifactTitle,
    Typography,
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return selectionStore.selectedArtifact;
    },
  },
});
</script>
