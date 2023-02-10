<template>
  <v-btn-toggle tile group multiple dense :value="value">
    <text-button
      :value="options.tim"
      text
      color="accent"
      data-cy="button-nav-tim"
      icon-id="mdi-ballot"
      @click="handleTimView"
    >
      TIM
    </text-button>
    <text-button
      :disabled="isTreeDisabled"
      :value="options.tree"
      text
      color="accent"
      data-cy="button-nav-tree"
      icon-id="mdi-family-tree"
      @click="handleTreeView"
    >
      Tree
    </text-button>
    <text-button
      :value="options.table"
      text
      color="accent"
      data-cy="button-nav-table"
      icon-id="mdi-table-multiple"
      @click="handleTableView"
    >
      Table
    </text-button>
    <text-button
      :disabled="isDeltaDisabled"
      :value="options.delta"
      text
      color="accent"
      data-cy="button-nav-delta"
      icon-id="mdi-compare"
      @click="handleDeltaView"
    >
      Delta
    </text-button>
  </v-btn-toggle>
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
import { computed, ref, onMounted, watch } from "vue";
import { GraphMode } from "@/types";
import { appStore, deltaStore, documentStore, layoutStore } from "@/hooks";
import { TextButton } from "@/components/common";

const options = {
  tim: GraphMode.tim,
  tree: GraphMode.tree,
  table: GraphMode.table,
  delta: GraphMode.delta,
};

const value = ref<GraphMode[]>([]);

const isTreeDisabled = computed(() => documentStore.isTableOnlyDocument);
const isDeltaDisabled = computed(() => layoutStore.mode === GraphMode.tim);

/**
 * Updates the values of which buttons are highlighted.
 */
function updateValue(): void {
  const selected: GraphMode[] = [];

  selected.push(layoutStore.mode);

  if (deltaStore.inDeltaView) {
    selected.push(GraphMode.delta);
  }

  value.value = selected;
}

/**
 * Opens tree view.
 */
function handleTimView(): void {
  layoutStore.mode = GraphMode.tim;
  updateValue();
}

/**
 * Opens tree view.
 */
function handleTreeView(): void {
  layoutStore.mode = GraphMode.tree;
  updateValue();
}

/**
 * Opens table view.
 */
function handleTableView(): void {
  layoutStore.mode = GraphMode.table;
  updateValue();
}
/**
 * Opens delta view.
 */
function handleDeltaView(): void {
  appStore.openDetailsPanel("delta");
  updateValue();
}

onMounted(() => updateValue());

watch(
  () => deltaStore.inDeltaView,
  () => updateValue()
);

watch(
  () => isTreeDisabled.value,
  () => updateValue()
);

watch(
  () => isDeltaDisabled.value,
  () => updateValue()
);
</script>
