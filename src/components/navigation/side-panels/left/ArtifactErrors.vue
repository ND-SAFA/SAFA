<template>
  <div v-if="selectedArtifactWarnings.length > 0">
    <flex-box>
      <v-icon color="secondary">mdi-hazard-lights</v-icon>
      <typography el="h2" l="1" variant="subtitle" value="Warnings" />
    </flex-box>

    <v-divider />

    <v-list expand>
      <v-list-group
        v-for="(warning, idx) in selectedArtifactWarnings"
        :key="idx"
      >
        <template v-slot:activator>
          <v-list-item-title>
            <typography :value="warning.ruleName" />
          </v-list-item-title>
        </template>
        <v-divider class="faded" />
        <typography :value="warning.ruleMessage" />
      </v-list-group>
    </v-list>
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
