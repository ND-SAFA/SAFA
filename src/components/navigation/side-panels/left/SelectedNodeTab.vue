<template>
  <v-container>
    <div v-if="selectedArtifact !== undefined">
      <artifact-title />
      <v-divider class="mb-2" />
      <p class="text-body-1">{{ selectedArtifact.body }}</p>
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
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
  },
});
</script>
