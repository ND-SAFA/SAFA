<template>
  <q-chip
    :color="timStore.getTypeColor(props.artifact.type, true)"
    :icon="timStore.getTypeIcon(props.artifact.type)"
    outline
    style="max-width: 300px; height: fit-content"
    clickable
  >
    <typography :value="props.artifact.name" wrap color="text" />
    <q-popup-proxy>
      <artifact-body-display
        clickable
        display-title
        :artifact="props.artifact"
        @click="selectionStore.selectArtifact(props.artifact.id)"
      />
    </q-popup-proxy>
  </q-chip>
</template>

<script lang="ts">
/**
 * Displays a chip for an artifact, which can be clicked to view the artifact in a popout.
 */
export default {
  name: "ArtifactChip",
};
</script>

<script setup lang="ts">
import { ArtifactProps } from "@/types";
import { selectionStore, timStore } from "@/hooks";
import { Typography } from "@/components/common";
import ArtifactBodyDisplay from "./ArtifactBodyDisplay.vue";

const props = defineProps<ArtifactProps>();
</script>
