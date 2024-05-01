<template>
  <q-page-sticky
    v-if="layoutStore.isTimMode || layoutStore.isTreeMode"
    position="top-right"
    class="artifact-fab"
  >
    <flex-box column x="2" y="2" align="end" style="width: 40px">
      <visible-type-buttons />
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
    </flex-box>
  </q-page-sticky>
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
import { LARGE_NODE_LAYOUT_COUNT } from "@/util";
import {
  artifactStore,
  cyStore,
  layoutApiStore,
  layoutStore,
  permissionStore,
} from "@/hooks";
import { IconButton, FlexBox } from "@/components/common";
import VisibleTypeButtons from "./VisibleTypeButtons.vue";

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
      if (
        layoutStore.isTreeMode &&
        artifactStore.currentArtifacts.length > LARGE_NODE_LAYOUT_COUNT
      ) {
        layoutApiStore.handleRegenerate();
      } else {
        layoutStore.setGraphLayout("project", true);
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
