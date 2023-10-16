<template>
  <flex-box v-if="!layoutStore.isTableMode">
    <separator vertical inset nav x="1" />
    <icon-button
      v-for="definition in viewButtons"
      :key="definition.label"
      color="text"
      :tooltip="definition.label"
      :icon="definition.icon"
      :disabled="definition.disabled"
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
import { cyStore, layoutApiStore, layoutStore, permissionStore } from "@/hooks";
import { IconButton, FlexBox, Separator } from "@/components/common";

const viewButtons = computed(() => [
  {
    handler: () => cyStore.zoom("in"),
    label: "Zoom In",
    icon: "graph-zoom-in" as IconVariant,
    disabled: layoutStore.isTableMode,
    dataCy: "button-nav-graph-zoom-in",
  },
  {
    handler: () => cyStore.zoom("out"),
    label: "Zoom Out",
    icon: "graph-zoom-out" as IconVariant,
    disabled: layoutStore.isTableMode,
    dataCy: "button-nav-graph-zoom-out",
  },
  {
    handler: () => cyStore.centerNodes(true),
    label: "Center Graph",
    icon: "graph-center" as IconVariant,
    disabled: layoutStore.isTableMode,
    dataCy: "button-nav-graph-center",
  },
  {
    handler: () => {
      if (layoutStore.isTreeMode) {
        layoutApiStore.handleRegenerate();
      } else {
        layoutStore.resetLayout();
      }
    },
    label: "Regenerate Layout",
    icon: "graph-refresh" as IconVariant,
    disabled:
      layoutStore.isTableMode ||
      !permissionStore.isAllowed("project.edit_data"),
    dataCy: "button-nav-graph-refresh",
  },
]);
</script>
