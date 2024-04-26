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
    <typography
      default-expanded
      :collapse-length="0"
      :variant="variant"
      el="p"
      class="full-width"
      :value="body"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's body.
 */
export default {
  name: "ArtifactBody",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { artifactStore } from "@/hooks";
import { Typography, PanelCard, Separator } from "@/components/common";
import ArtifactNameDisplay from "./ArtifactNameDisplay.vue";

const artifact = computed(() => artifactStore.selectedArtifact);

const body = computed(() => artifact.value?.body.trim() || "");

const variant = computed(() =>
  artifact.value?.isCode ? "code" : "expandable"
);
</script>
