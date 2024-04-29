<template>
  <q-btn-group flat class="q-mx-sm nav-mode-select">
    <text-button
      v-bind="buttonProps(options.tim)"
      :hide-label="smallWindow"
      label="Types"
      data-cy="button-nav-tim"
      icon="view-tim"
      @click="handleTimView"
    >
      <q-tooltip> The types of artifacts and how they relate </q-tooltip>
    </text-button>
    <text-button
      v-bind="buttonProps(options.tree)"
      :hide-label="smallWindow"
      :disabled="artifactStore.largeNodeCount"
      label="Tree"
      data-cy="button-nav-tree"
      icon="view-tree"
      @click="handleTreeView"
    >
      <q-tooltip> {{ treeTooltip }} </q-tooltip>
    </text-button>
    <text-button
      v-bind="buttonProps(options.table)"
      :hide-label="smallWindow"
      :disabled="artifactStore.allArtifacts.length === 0"
      label="Table"
      data-cy="button-nav-table"
      icon="view-table"
      @click="handleTableView"
    >
      <q-tooltip> Tables of artifacts and trace links </q-tooltip>
    </text-button>
    <delta-mode-button
      v-bind="buttonProps(options.delta)"
      :hide-label="smallWindow"
      @click="handleDeltaView"
    />
  </q-btn-group>
</template>

<script lang="ts">
/**
 * Buttons for changing the mode of the artifact view.
 */
export default {
  name: "ModeButtons",
};
</script>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { GraphMode } from "@/types";
import {
  appStore,
  artifactStore,
  deltaStore,
  layoutStore,
  useScreen,
} from "@/hooks";
import { TextButton } from "@/components/common";
import DeltaModeButton from "./DeltaModeButton.vue";

const options: Record<GraphMode, GraphMode> = {
  tim: "tim",
  tree: "tree",
  table: "table",
  delta: "delta",
};

const { smallWindow } = useScreen();

const value = ref<GraphMode[]>([]);

const treeTooltip = computed(() => {
  return artifactStore.largeNodeCount
    ? "The tree view is disabled for very large graphs. " +
        'To view a tree, visit "Table" view and select the tree icon next to an artifact, or create a new custom "View" above.'
    : "A graph of related artifacts";
});

/**
 * Returns props for a mode button.
 * @param option - The mode button to get props for.
 */
function buttonProps(option: GraphMode) {
  const selected = value.value.includes(option);

  return {
    text: !selected,
    color: selected ? undefined : "text",
    class: selected ? "button-group-selected text-primary" : "",
  };
}

/**
 * Updates the values of which buttons are highlighted.
 */
function updateValue(): void {
  const selected: GraphMode[] = [];

  selected.push(layoutStore.mode);

  if (deltaStore.inDeltaView) {
    selected.push("delta");
  }

  value.value = selected;
}

/**
 * Opens tree view.
 */
function handleTimView(): void {
  layoutStore.mode = "tim";
}

/**
 * Opens tree view.
 */
function handleTreeView(): void {
  layoutStore.mode = "tree";

  appStore.closeSidePanels();
}

/**
 * Opens table view.
 */
function handleTableView(): void {
  layoutStore.mode = "table";

  appStore.closeSidePanels();
}
/**
 * Opens delta view.
 */
function handleDeltaView(): void {
  if (!deltaStore.inDeltaView) return;

  appStore.openDetailsPanel("delta");
  updateValue();
}

onMounted(() => updateValue());

watch(
  () => layoutStore.mode,
  () => updateValue()
);

watch(
  () => deltaStore.inDeltaView,
  () => updateValue()
);
</script>
