<template>
  <q-btn-group flat>
    <text-button
      :text="!value.includes(options.tim)"
      :outlined="value.includes(options.tim)"
      color="accent"
      data-cy="button-nav-tim"
      variant="view-tim"
      @click="handleTimView"
    >
      TIM
    </text-button>
    <text-button
      :disabled="isTreeDisabled"
      :text="!value.includes(options.tree)"
      :outlined="value.includes(options.tree)"
      color="accent"
      data-cy="button-nav-tree"
      variant="view-tree"
      @click="handleTreeView"
    >
      Tree
    </text-button>
    <text-button
      :text="!value.includes(options.table)"
      :outlined="value.includes(options.table)"
      color="accent"
      data-cy="button-nav-table"
      variant="view-table"
      @click="handleTableView"
    >
      Table
    </text-button>
    <text-button
      :disabled="isDeltaDisabled"
      :text="!value.includes(options.delta)"
      :outlined="value.includes(options.delta)"
      color="accent"
      data-cy="button-nav-delta"
      variant="view-delta"
      @click="handleDeltaView"
    >
      Delta
    </text-button>
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
