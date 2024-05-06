<template>
  <q-chip
    :color="color"
    :icon="timStore.getTypeIcon(props.artifact.type)"
    outline
    style="max-width: 300px; height: fit-content"
    clickable
  >
    <artifact-name-display :artifact="props.artifact" />
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
import { computed } from "vue";
import { ArtifactProps, ColorProps } from "@/types";
import { selectionStore, timStore } from "@/hooks";
import ArtifactNameDisplay from "./ArtifactNameDisplay.vue";
import ArtifactBodyDisplay from "./ArtifactBodyDisplay.vue";

const props = defineProps<ArtifactProps & ColorProps>();

const color = computed(
  () => props.color || timStore.getTypeColor(props.artifact.type, true)
);
</script>
