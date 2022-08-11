<template>
  <div v-if="selectedArtifactWarnings.length > 0">
    <flex-box>
      <v-icon color="secondary">mdi-hazard-lights</v-icon>
      <typography el="h2" l="1" variant="subtitle" value="Warnings" />
    </flex-box>

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
import { Typography, FlexBox } from "@/components/common";

/**
 * Displays the selected node's error.
 */
export default Vue.extend({
  name: "ArtifactErrors",
  components: { FlexBox, Typography },
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
