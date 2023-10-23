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
        v-for="{ type, count } in artifacts"
        :key="type"
        :count="count"
        :artifact-type="type"
      />
      <tim-link
        v-for="{ name, sourceType, targetType, count, isGenerated } in traces"
        :key="name"
        :count="count"
        :target-type="targetType"
        :source-type="sourceType"
        :generated="isGenerated"
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
import { computed, onMounted, ref } from "vue";
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

const artifacts = computed(() =>
  projectSaveStore.artifactPanels
    .filter(({ valid }) => valid)
    .map(({ type, artifacts = [] }) => ({
      type,
      count: artifacts.length,
    }))
);

const traces = computed(() =>
  projectSaveStore.tracePanels
    .filter(({ valid }) => valid)
    .map(({ name, type, toType = "", traces = [], isGenerated }) => ({
      name,
      sourceType: type,
      targetType: toType,
      count: traces.length,
      isGenerated,
    }))
);

onMounted(() => {
  layoutStore.setGraphLayout("creator");
});
</script>
