<template>
  <panel-card>
    <flex-box align="center" justify="space-between">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <typography
            ellipsis
            v-on="on"
            v-bind="attrs"
            variant="subtitle"
            el="h1"
            :value="selectedArtifactName"
            data-cy="text-selected-name"
          />
        </template>
        {{ selectedArtifactName }}
      </v-tooltip>
      <attribute-chip
        artifact-type
        :value="selectedArtifactType"
        data-cy="text-selected-type"
      />
    </flex-box>

    <v-divider />

    <typography variant="caption" value="Body" />
    <typography
      defaultExpanded
      variant="expandable"
      :value="selectedArtifactBody"
      data-cy="text-selected-body"
    />

    <attribute-list-display class="mt-4" :artifact="selectedArtifact" />
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { selectionStore } from "@/hooks";
import {
  Typography,
  FlexBox,
  AttributeChip,
  PanelCard,
  AttributeListDisplay,
} from "@/components/common";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactFields",
  components: {
    AttributeListDisplay,
    PanelCard,
    AttributeChip,
    FlexBox,
    Typography,
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's name.
     */
    selectedArtifactName(): string {
      return this.selectedArtifact?.name || "";
    },
    /**
     * @return The selected artifact's type.
     */
    selectedArtifactType(): string {
      return this.selectedArtifact?.type || "";
    },
    /**
     * @return The selected artifact's body.
     */
    selectedArtifactBody(): string {
      return this.selectedArtifact?.body.trim() || "";
    },
  },
});
</script>

<style scoped>
.artifact-title {
  width: 230px;
}
</style>
