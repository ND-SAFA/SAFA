<template>
  <div v-if="isOpen">
    <panel-card class="mt-2">
      <attribute-chip artifact-type :value="artifactType" />
      <v-divider class="mt-1" />
      <typography variant="caption" value="Details" />
      <typography el="p" :value="artifactCount" />
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore, selectionStore } from "@/hooks";
import { PanelCard, AttributeChip, Typography } from "@/components/common";

/**
 * Displays artifact level information.
 */
export default Vue.extend({
  name: "ArtifactLevelPanel",
  components: { PanelCard, AttributeChip, Typography },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayArtifactLevel";
    },
    /**
     * @return The selected artifact type.
     */
    artifactType(): string {
      return selectionStore.selectedArtifactType;
    },
    /**
     * @return The number of artifacts of the selected type.
     */
    artifactCount(): string {
      const count = selectionStore.selectedArtifactLevel?.count || 0;

      return count === 1 ? "1 Artifact" : `${count} Artifacts`;
    },
  },
});
</script>
