<template>
  <div v-if="selectedArtifactWarnings.length > 0">
    <flex-box data-cy="artifact-warnings">
      <v-icon color="secondary">mdi-hazard-lights</v-icon>
      <typography
        el="h2"
        l="1"
        variant="subtitle"
        value="Warnings"
        data-cy="artifact-table-panel-warnings-title"
      />
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
import { warningStore, selectionStore } from "@/hooks";
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
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's warnings.
     */
    selectedArtifactWarnings(): WarningModel[] {
      const id = this.selectedArtifact?.id || "";

      return warningStore.artifactWarnings[id] || [];
    },
  },
});
</script>
