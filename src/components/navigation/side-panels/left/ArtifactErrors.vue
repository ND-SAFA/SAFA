<template>
  <div v-if="selectedArtifactWarnings.length > 0">
    <flex-box>
      <v-icon color="secondary">mdi-hazard-lights</v-icon>
      <typography el="h2" l="1" variant="subtitle" value="Warnings" />
    </flex-box>

    <v-divider />

    <v-list expand>
      <toggle-list
        v-for="(warning, idx) in selectedArtifactWarnings"
        :key="idx"
        :title="warning.ruleName"
      >
        <typography :value="warning.ruleMessage" />
      </toggle-list>
    </v-list>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { WarningModel } from "@/types";
import { artifactSelectionModule, errorModule } from "@/store";
import { Typography, FlexBox, ToggleList } from "@/components/common";

/**
 * Displays the selected node's error.
 */
export default Vue.extend({
  name: "ArtifactErrors",
  components: { ToggleList, FlexBox, Typography },
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
    selectedArtifactWarnings(): WarningModel[] {
      const id = this.selectedArtifact?.id || "";

      return errorModule.getArtifactWarnings[id] || [];
    },
  },
});
</script>
