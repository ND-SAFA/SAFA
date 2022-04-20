<template>
  <v-expansion-panels>
    <v-expansion-panel
      v-for="warning in selectedArtifactWarnings"
      :key="warning"
    >
      <v-expansion-panel-header class="text-body-1">
        {{ warning.ruleName }}
      </v-expansion-panel-header>
      <v-expansion-panel-content class="text-body-1">
        {{ warning.ruleMessage }}
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
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

<style scoped>
.v-expansion-panel::before {
  box-shadow: none;
}
</style>
