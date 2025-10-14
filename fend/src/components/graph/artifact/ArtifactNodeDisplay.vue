<template>
  <node-display
    separator
    :color="props.color"
    variant="artifact"
    :title="props.artifact.type"
    :selected="props.selected"
    @click="handleSelect"
    @dblclick="handleSelect(true)"
  >
    <artifact-name-display
      align="center"
      :artifact="props.artifact"
      is-header
      dense
      class="cy-node-artifact-name"
      data-cy="tree-node-name"
    />
    <separator
      v-if="showDelta"
      :color="props.deltaColor"
      class="cy-node-delta-chip"
    />
  </node-display>
</template>

<script lang="ts">
/**
 * Renders the identifying content of an artifact node in the graph.
 */
export default {
  name: "ArtifactNodeDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactNodeDisplayProps } from "@/types";
import { deltaStore, selectionStore, viewsStore } from "@/hooks";
import { NodeDisplay } from "@/components/graph/display";
import { Separator } from "@/components/common";
import { ArtifactNameDisplay } from "@/components/artifact";

const props = defineProps<Omit<ArtifactNodeDisplayProps, "hiddenChildren">>();

const id = computed(() => props.artifact.id);
const showDelta = computed(() => deltaStore.inDeltaView);

/**
 * Selects an artifact and highlights its subtree,
 * or opens a new view of the artifact's subtree if the artifact is already selected.
 */
function handleSelect(selected = props.selected): void {
  if (!selected) {
    selectionStore.selectArtifact(id.value);
  } else {
    viewsStore.addDocumentOfNeighborhood({
      id: id.value,
      name: props.artifact.name,
    });
  }
}
</script>
