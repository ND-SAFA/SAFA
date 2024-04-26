<template>
  <panel-card borderless>
    <artifact-name-display
      v-if="artifact"
      :artifact="artifact"
      display-type
      display-tooltip
      is-header
      data-cy-name="text-selected-name"
      data-cy-type="text-selected-type"
    />

    <separator b="2" t="1" />

    <typography variant="caption" value="Body" />
    <typography
      default-expanded
      :collapse-length="0"
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
  name: "ArtifactContent",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { artifactStore } from "@/hooks";
import {
  Typography,
  PanelCard,
  AttributeListDisplay,
  Separator,
} from "@/components/common";
import { ArtifactSummary } from "@/components/artifact/save";
import ArtifactNameDisplay from "./ArtifactNameDisplay.vue";

const artifact = computed(() => artifactStore.selectedArtifact);
const body = computed(() => artifact.value?.body.trim() || "");
const isCode = computed(() => !!artifact.value?.isCode);
const variant = computed(() => (isCode.value ? "code" : "expandable"));
</script>
