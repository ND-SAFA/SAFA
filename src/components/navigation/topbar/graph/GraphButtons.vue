<template>
  <flex-box>
    <checkmark-menu
      :key="filterButton.label"
      :definition="filterButton"
      :is-disabled="isButtonDisabled(filterButton)"
    />
    <v-divider inset vertical class="text-accent mx-1 mb-2" />
    <template v-for="definition in viewButtons">
      <icon-button
        v-if="definition.handler"
        :key="definition.label"
        color="accent"
        :tooltip="definition.label"
        :icon-id="definition.icon"
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
import { computed, onMounted, ref, watch } from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import { layoutStore, selectionStore, artifactStore } from "@/hooks";
import { handleRegenerateLayout } from "@/api";
import { cyCenterNodes, cyZoomIn, cyZoomOut } from "@/cytoscape";
import { IconButton, CheckmarkMenu, FlexBox } from "@/components/common";

const viewButtons: ButtonDefinition[] = [
  {
    type: ButtonType.ICON,
    handler: () => cyZoomIn(),
    label: "Zoom In",
    icon: "mdi-magnify-plus-outline",
  },
  {
    type: ButtonType.ICON,
    handler: () => cyZoomOut(),
    label: "Zoom Out",
    icon: "mdi-magnify-minus-outline",
  },
  {
    type: ButtonType.ICON,
    handler: () => cyCenterNodes(true),
    label: "Center Graph",
    icon: "mdi-graphql",
    dataCy: "button-nav-graph-center",
  },
  {
    type: ButtonType.ICON,
    handler: () => handleRegenerateLayout({}),
    label: "Regenerate Layout",
    icon: "mdi-refresh",
  },
];

const menuItems = ref<[string, boolean][]>([]);

const filterButton = computed<ButtonDefinition>(() => ({
  type: ButtonType.CHECKMARK_MENU,
  label: "Filter Artifacts",
  icon: "mdi-filter",
  dataCy: "button-nav-graph-filter",
  menuItems: menuItems.value.map(([name], itemIndex) => ({
    name,
    onClick: () => filterItem(itemIndex),
  })),
  checkmarkValues: menuItems.value.map((i) => i[1]),
}));

/**
 * @return Whether to disable a graph button.
 */
function isButtonDisabled(button: ButtonDefinition): boolean {
  return button.isDisabled || layoutStore.isTableMode;
}

/**
 * Filters the visible artifacts on the graph.
 * @param index - The index of the type to change filtering for.
 */
function filterItem(index: number) {
  const [type, oldState] = menuItems.value[index];
  const newState = !oldState;

  menuItems.value[index] = [type, newState];

  selectionStore.filterGraph({
    type: "ignore",
    ignoreType: type,
    action: newState ? "remove" : "add",
  });
}

/**
 * Creates saved state for the graph menu items.
 */
function refreshMenuItems(): [string, boolean][] {
  return Array.from(
    new Set(artifactStore.currentArtifacts.map((a) => a.type))
  ).map((i) => [i, true]);
}

onMounted(() => refreshMenuItems());

watch(
  () => artifactStore.currentArtifacts,
  () => refreshMenuItems()
);
</script>
