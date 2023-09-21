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
    <panel-card>
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
    </panel-card>
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
import { computed, ref, watch } from "vue";
import { TimTreeProps } from "@/types";
import { appStore, layoutStore, projectSaveStore, cyStore } from "@/hooks";
import { FlexBox, TextButton, PanelCard } from "@/components/common";
import { Cytoscape } from "./base";
import { TimNode, TimLink } from "./tim";

const props = defineProps<TimTreeProps>();

const graph = ref(cyStore.buildCreatorGraph());

const className = computed(() => {
  if (!props.visible) {
    return "artifact-view disabled";
  } else if (!appStore.isLoading) {
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

watch(
  () => props.visible,
  () => {
    if (!props.visible) return;

    layoutStore.setGraphLayout("creator");
  }
);
</script>
