<template>
  <div v-if="selectedArtifactWarnings.length > 0">
    <div class="d-flex flex-row">
      <v-icon color="secondary">mdi-hazard-lights</v-icon>
      <typography el="h2" l="1" variant="subtitle" value="Warnings" />
    </div>

    <v-divider class="mb-2" />

    <v-expansion-panels>
      <v-expansion-panel
        v-for="(warning, idx) in selectedArtifactWarnings"
        :key="idx"
      >
        <v-expansion-panel-header>
          <typography :value="warning.ruleName" />
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <typography :value="warning.ruleMessage" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactWarning } from "@/types";
import { artifactSelectionModule, errorModule } from "@/store";
import { Typography } from "@/components/common";

/**
 * Displays the selected node's error.
 */
export default Vue.extend({
  name: "ArtifactErrors",
  components: { Typography },
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
