<template>
  <div v-if="isOpen">
    <flex-box t="2">
      <text-button text variant="artifact" @click="handleViewLevel">
        View In Tree
      </text-button>
    </flex-box>
    <panel-card class="mt-2" data-cy="panel-artifact-type">
      <attribute-chip artifact-type :value="artifactLevel.name" />
      <v-divider class="mt-1" />
      <typography variant="caption" value="Details" />
      <typography el="p" :value="artifactCount" />
    </panel-card>
    <panel-card class="mt-2" data-cy="panel-artifact-type-options">
      <typography variant="subtitle" value="Type Options" />
      <v-divider class="my-1" />
      <type-direction-input v-if="artifactLevel" :entry="artifactLevel" />
      <type-icon-input v-if="artifactLevel" :entry="artifactLevel" />
    </panel-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { TimArtifactLevelSchema } from "@/types";
import { appStore, layoutStore, selectionStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  TypeDirectionInput,
  TypeIconInput,
  TextButton,
  FlexBox,
} from "@/components/common";

/**
 * Displays artifact level information.
 */
export default defineComponent({
  name: "ArtifactLevelPanel",
  components: {
    TextButton,
    FlexBox,
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
     * @return The selected trace matrix.
     */
    artifactLevel(): TimArtifactLevelSchema | undefined {
      return selectionStore.selectedArtifactLevel;
    },
    /**
     * @return The number of artifacts of the selected type.
     */
    artifactCount(): string {
      const count = this.artifactLevel?.count || 0;

      return count === 1 ? "1 Artifact" : `${count} Artifacts`;
    },
  },
  methods: {
    /**
     * Switches to tree view and highlights this type level.
     */
    handleViewLevel(): void {
      if (!this.artifactLevel) return;

      layoutStore.viewTreeTypes([this.artifactLevel.name]);
    },
  },
});
</script>
