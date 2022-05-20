<template>
  <div v-if="selectedArtifactWarnings.length > 0">
    <div class="d-flex flex-row">
      <v-icon color="secondary">mdi-hazard-lights</v-icon>
      <h2 class="text-h6 ml-1">Warnings</h2>
    </div>

    <v-divider class="mb-2" />

    <v-expansion-panels>
      <v-expansion-panel
        v-for="(warning, idx) in selectedArtifactWarnings"
        :key="idx"
      >
        <v-expansion-panel-header class="text-body-1">
          {{ warning.ruleName }}
        </v-expansion-panel-header>
        <v-expansion-panel-content class="text-body-1">
          {{ warning.ruleMessage }}
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactWarning } from "@/types";
import { artifactSelectionModule, errorModule } from "@/store";

/**
 * Displays the selected node's error.
 */
export default Vue.extend({
  name: "ArtifactErrors",
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact's warnings.
     */
    selectedArtifactWarnings(): ArtifactWarning[] {
      const id = this.selectedArtifact?.id || "";

      return errorModule.getArtifactWarnings[id] || [];
    },
  },
});
</script>
