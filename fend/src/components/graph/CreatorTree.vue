<template>
  <div>
    <flex-box justify="between" align="center">
      <typography variant="subtitle" value="Artifact Type Tree" />
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
import Typography from "@/components/common/display/content/Typography.vue";
import { Cytoscape } from "./base";
import { TimNode, TimLink } from "./tim";

const graph = ref(cyStore.buildCreatorGraph());
const loading = ref(false);

const className = computed(() => {
  if (!appStore.isLoading && !loading.value) {
    return "artifact-view visible";
  } else {
    return "artifact-view";
  }
});

onMounted(() => {
  layoutStore.setGraphLayout("creator");
});

watch(
  () => [projectSaveStore.graphNodes, projectSaveStore.graphEdges],
  () => {
    loading.value = true;

    // Wait for 0.1s width animation before resetting the layout.
    setTimeout(() => {
      layoutStore.setGraphLayout("creator");
      loading.value = false;
    }, 100);
  }
);
</script>
