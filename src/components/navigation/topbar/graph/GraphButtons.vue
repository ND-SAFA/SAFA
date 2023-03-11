<template>
  <flex-box>
    <template v-for="definition in viewButtons" :key="definition.label">
      <icon-button
        color="accent"
        :tooltip="definition.label"
        :icon="definition.icon"
        :disabled="isDisabled"
        :data-cy="definition.dataCy"
        @click="definition.handler"
      />
    </template>
  </flex-box>
</template>

<script lang="ts">
/**
 * Renders buttons for changing the graph view.
 */
export default {
  name: "GraphButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { layoutStore } from "@/hooks";
import { handleRegenerateLayout } from "@/api";
import { cyCenterNodes, cyZoomIn, cyZoomOut } from "@/cytoscape";
import { IconButton, FlexBox } from "@/components/common";

const viewButtons = [
  {
    handler: () => cyZoomIn(),
    label: "Zoom In",
    icon: "graph-zoom-in",
  },
  {
    handler: () => cyZoomOut(),
    label: "Zoom Out",
    icon: "graph-zoom-out",
  },
  {
    handler: () => cyCenterNodes(true),
    label: "Center Graph",
    icon: "graph-center",
    dataCy: "button-nav-graph-center",
  },
  {
    handler: () => handleRegenerateLayout({}),
    label: "Regenerate Layout",
    icon: "graph-refresh",
  },
];

const isDisabled = computed(() => layoutStore.isTableMode);
</script>
