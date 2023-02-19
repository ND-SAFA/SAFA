<template>
  <flex-box>
    <template v-for="definition in viewButtons" :key="definition.label">
      <icon-button
        color="accent"
        :tooltip="definition.label"
        :icon="definition.icon"
        :is-disabled="isButtonDisabled(definition)"
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
import { ButtonDefinition, ButtonType } from "@/types";
import { layoutStore } from "@/hooks";
import { handleRegenerateLayout } from "@/api";
import { cyCenterNodes, cyZoomIn, cyZoomOut } from "@/cytoscape";
import { IconButton, FlexBox } from "@/components/common";

const viewButtons: ButtonDefinition[] = [
  {
    type: ButtonType.ICON,
    handler: () => cyZoomIn(),
    label: "Zoom In",
    icon: "graph-zoom-in",
  },
  {
    type: ButtonType.ICON,
    handler: () => cyZoomOut(),
    label: "Zoom Out",
    icon: "graph-zoom-out",
  },
  {
    type: ButtonType.ICON,
    handler: () => cyCenterNodes(true),
    label: "Center Graph",
    icon: "graph-center",
    dataCy: "button-nav-graph-center",
  },
  {
    type: ButtonType.ICON,
    handler: () => handleRegenerateLayout({}),
    label: "Regenerate Layout",
    icon: "graph-refresh",
  },
];

/**
 * @return Whether to disable a graph button.
 */
function isButtonDisabled(button: ButtonDefinition): boolean {
  return button.isDisabled || layoutStore.isTableMode;
}
</script>
