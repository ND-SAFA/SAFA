<template>
  <v-container>
    <flex-box justify="end">
      <v-btn text @click="cyResetTim"> Reset Graph </v-btn>
    </flex-box>
    <cytoscape-controller
      id="cytoscape-tim"
      :cyto-core-graph="timGraph"
      :class="className"
    >
      <template #elements>
        <tim-node
          v-for="panel in artifactPanels"
          :key="panel.title"
          :count="panel.projectFile.artifacts.length"
          :artifact-type="panel.projectFile.type"
        />
        <tim-link
          v-for="panel in tracePanels"
          :key="panel.projectFile.sourceId + panel.projectFile.targetId"
          :count="panel.projectFile.traces.length"
          :target-type="panel.projectFile.targetId"
          :source-type="panel.projectFile.sourceId"
          :generated="panel.projectFile.isGenerated"
        />
      </template>
    </cytoscape-controller>
  </v-container>
</template>

<script lang="ts">
/**
 * Creates a Cytoscape graph containing artifact types are nodes
 * and links between them as edges.
 */
export default {
  name: "TimTree",
};
</script>

<script setup lang="ts">
import { computed, defineProps, watch } from "vue";
import { TracePanel, ArtifactPanel } from "@/types";
import { appStore, layoutStore } from "@/hooks";
import { timGraph, cyResetTim } from "@/cytoscape";
import { FlexBox } from "@/components/common/layout";
import CytoscapeController from "./CytoscapeController.vue";
import { TimNode, TimLink } from "./tim";

const props = defineProps<{
  tracePanels: TracePanel[];
  artifactPanels: ArtifactPanel[];
  inView: boolean;
}>();

const className = computed(() => {
  if (!props.inView) {
    return "artifact-view disabled";
  } else if (!appStore.isLoading) {
    return "artifact-view visible elevation-3";
  } else {
    return "artifact-view";
  }
});

watch(
  () => props.inView,
  (inView) => {
    if (!inView) return;

    layoutStore.setTimTreeLayout();
  }
);
</script>
