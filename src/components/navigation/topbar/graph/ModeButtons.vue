<template>
  <q-btn-group flat class="q-mx-sm nav-mode-select">
    <text-button
      v-bind="buttonProps(options.tim)"
      :hide-label="smallWindow"
      label="TIM"
      data-cy="button-nav-tim"
      icon="view-tim"
      @click="handleTimView"
    />
    <text-button
      v-bind="buttonProps(options.tree)"
      :disabled="isTreeDisabled"
      :hide-label="smallWindow"
      label="Tree"
      data-cy="button-nav-tree"
      icon="view-tree"
      @click="handleTreeView"
    />
    <text-button
      v-bind="buttonProps(options.table)"
      :hide-label="smallWindow"
      label="Table"
      data-cy="button-nav-table"
      icon="view-table"
      @click="handleTableView"
    />
    <text-button
      v-bind="buttonProps(options.delta)"
      :hide-label="smallWindow"
      label="Delta"
      data-cy="button-nav-delta"
      icon="view-delta"
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
import { computed, ref, onMounted, watch } from "vue";
import { GraphMode } from "@/types";
import {
  appStore,
  deltaStore,
  documentStore,
  layoutStore,
  useScreen,
} from "@/hooks";
import { TextButton } from "@/components/common";

const options = {
  tim: GraphMode.tim,
  tree: GraphMode.tree,
  table: GraphMode.table,
  delta: GraphMode.delta,
};

const { smallWindow } = useScreen();

const value = ref<GraphMode[]>([]);

const isTreeDisabled = computed(() => documentStore.isTableOnlyDocument);

/**
 * Returns props for a mode button.
 * @param option - The mode button to get props for.
 */
function buttonProps(option: GraphMode) {
  const selected = value.value.includes(option);

  return {
    text: !selected,
    outlined: selected,
    color: "primary",
    class: selected ? "nav-mode-selected" : "",
  };
}

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
  () => layoutStore.mode,
  () => updateValue()
);

watch(
  () => deltaStore.inDeltaView,
  () => updateValue()
);

watch(
  () => isTreeDisabled.value,
  () => updateValue()
);
</script>
