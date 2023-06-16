<template>
  <flex-box v-if="!isDisabled">
    <separator vertical inset nav x="1" />
    <icon-button
      v-for="definition in viewButtons"
      :key="definition.label"
      color="primary"
      :tooltip="definition.label"
      :icon="definition.icon"
      :data-cy="definition.dataCy"
      @click="definition.handler"
    />
    <separator vertical inset nav x="1" />
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
import { IconVariant } from "@/types";
import { layoutApiStore, layoutStore } from "@/hooks";
import { cyCenterNodes, cyZoomIn, cyZoomOut } from "@/cytoscape";
import { IconButton, FlexBox, Separator } from "@/components/common";

const viewButtons = [
  {
    handler: () => cyZoomIn(),
    label: "Zoom In",
    icon: "graph-zoom-in" as IconVariant,
    dataCy: "button-nav-graph-zoom-in",
  },
  {
    handler: () => cyZoomOut(),
    label: "Zoom Out",
    icon: "graph-zoom-out" as IconVariant,
    dataCy: "button-nav-graph-zoom-out",
  },
  {
    handler: () => cyCenterNodes(true),
    label: "Center Graph",
    icon: "graph-center" as IconVariant,
    dataCy: "button-nav-graph-center",
  },
  {
    handler: () => {
      if (layoutStore.isTreeMode) {
        layoutApiStore.handleRegenerateLayout();
      } else {
        layoutStore.resetLayout();
      }
    },
    label: "Regenerate Layout",
    icon: "graph-refresh" as IconVariant,
    dataCy: "button-nav-graph-refresh",
  },
];

const isDisabled = computed(() => layoutStore.isTableMode);
</script>
