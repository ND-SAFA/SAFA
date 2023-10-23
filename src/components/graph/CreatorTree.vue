<template>
  <div>
    <flex-box justify="end">
      <text-button
        text
        label="Center Graph"
        icon="graph-center"
        @click="cyStore.resetWindow('creator')"
      />
    </flex-box>
    <separator />
    <cytoscape
      id="cytoscape-tim"
      :graph="graph"
      :class="className"
      data-cy="view-tim-tree"
    >
      <tim-node
        v-for="node in projectSaveStore.graphNodes"
        :key="node.artifactType"
        v-bind="node"
      />
      <tim-link
        v-for="edge in projectSaveStore.graphEdges"
        :key="edge.sourceType + edge.targetType"
        v-bind="edge"
      />
    </cytoscape>
  </div>
</template>

<script lang="ts">
/**
 * Creates a Cytoscape graph containing artifact types are nodes
 * and links between them as edges.
 */
export default {
  name: "CreatorTree",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { appStore, layoutStore, projectSaveStore, cyStore } from "@/hooks";
import { FlexBox, TextButton, Separator } from "@/components/common";
import { Cytoscape } from "./base";
import { TimNode, TimLink } from "./tim";

const graph = ref(cyStore.buildCreatorGraph());

const className = computed(() => {
  if (!appStore.isLoading) {
    return "artifact-view visible elevation-3";
  } else {
    return "artifact-view";
  }
});

onMounted(() => {
  layoutStore.setGraphLayout("creator");
});

watch(
  () => [projectSaveStore.graphNodes, projectSaveStore.graphEdges],
  () => layoutStore.setGraphLayout("creator")
);
</script>
