<template>
  <panel-card>
    <artifact-name-display
      v-if="artifact"
      :artifact="artifact"
      display-type
      display-tooltip
      is-header
    />

    <separator b="2" t="1" />

    <typography variant="caption" value="Body" />
    <typography
      default-expanded
      :variant="variant"
      :value="body"
      data-cy="text-selected-body"
    />

    <artifact-summary />

    <attribute-list-display v-if="!!artifact" :artifact="artifact" />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's title and option buttons.
 */
export default {
  name: "ArtifactFields",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { selectionStore } from "@/hooks";
import {
  Typography,
  PanelCard,
  AttributeListDisplay,
  Separator,
} from "@/components/common";
import ArtifactNameDisplay from "./ArtifactNameDisplay.vue";
import ArtifactSummary from "./ArtifactSummary.vue";

const artifact = computed(() => selectionStore.selectedArtifact);
const body = computed(() => artifact.value?.body.trim() || "");
const isCode = computed(() => !!artifact.value?.isCode);
const variant = computed(() => (isCode.value ? "code" : "expandable"));
</script>
