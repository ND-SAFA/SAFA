<template>
  <v-container class="mb-10">
    <div v-if="selectedArtifact !== undefined">
      <artifact-title />
      <v-divider />
      <typography
        defaultExpanded
        y="2"
        variant="expandable"
        :value="artifactBody"
      />
      <artifact-traces />
      <artifact-documents />
      <artifact-errors />
    </div>

    <p v-else class="text-caption">No artifact is selected.</p>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { artifactSelectionModule } from "@/store";
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
      return artifactSelectionModule.getSelectedArtifact;
    },
    artifactBody(): string {
      const isCode = this.selectedArtifact?.type.toLowerCase().includes("code");

      return isCode ? "" : this.selectedArtifact?.body || "";
    },
  },
});
</script>
