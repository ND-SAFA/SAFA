<template>
  <panel-card>
    <flex-box align="center" justify="space-between">
      <v-tooltip bottom>
        <template #activator="{ props }">
          <typography
            ellipsis
            v-bind="props"
            variant="subtitle"
            el="h1"
            :value="name"
            data-cy="text-selected-name"
          />
        </template>
        {{ name }}
      </v-tooltip>
      <attribute-chip
        artifact-type
        :value="type"
        data-cy="text-selected-type"
      />
    </flex-box>

    <v-divider />

    <typography variant="caption" value="Body" />
    <typography
      default-expanded
      :variant="variant"
      :value="body"
      data-cy="text-selected-body"
    />

    <attribute-list-display class="mt-4" :artifact="artifact" />
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ReservedArtifactType, TextType } from "@/types";
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
export default defineComponent({
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
    artifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's name.
     */
    name(): string {
      return this.artifact?.name || "";
    },
    /**
     * @return The selected artifact's type.
     */
    type(): string {
      return this.artifact?.type || "";
    },
    /**
     * @return The selected artifact's body text variant.
     */
    variant(): TextType {
      return this.type === ReservedArtifactType.github ? "code" : "expandable";
    },
    /**
     * @return The selected artifact's body.
     */
    body(): string {
      return this.artifact?.body.trim() || "";
    },
  },
});
</script>
