<template>
  <div v-if="isOpen">
    <panel-card class="mt-2">
      <attribute-chip artifact-type :value="artifactType" />
      <v-divider class="mt-1" />
      <typography variant="caption" value="Details" />
      <typography el="p" :value="artifactCount" />
    </panel-card>
    <panel-card class="mt-2">
      <typography variant="subtitle" value="Type Options" />
      <v-divider class="my-1" />
      <type-direction-input v-if="typeDirection" :entry="typeDirection" />
      <type-icon-input v-if="typeDirection" :entry="typeDirection" />
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { LabelledTraceDirectionSchema } from "@/types";
import { appStore, selectionStore, typeOptionsStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  TypeDirectionInput,
  TypeIconInput,
} from "@/components/common";

/**
 * Displays artifact level information.
 */
export default Vue.extend({
  name: "ArtifactLevelPanel",
  components: {
    PanelCard,
    AttributeChip,
    Typography,
    TypeDirectionInput,
    TypeIconInput,
  },
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
     * @return The selected trace matrix.
     */
    typeDirection(): LabelledTraceDirectionSchema | undefined {
      return typeOptionsStore
        .typeDirections()
        .find(({ type }) => type === this.artifactType);
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
