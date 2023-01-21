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
import Vue from "vue";
import { GraphMode } from "@/types";
import { appStore, deltaStore, documentStore, layoutStore } from "@/hooks";
import { TextButton } from "@/components/common";

/**
 * Buttons for changing the mode of the artifact view.
 */
export default Vue.extend({
  name: "ModeButtons",
  components: { TextButton },
  data() {
    return {
      value: [] as GraphMode[],
      options: {
        tim: GraphMode.tim,
        tree: GraphMode.tree,
        table: GraphMode.table,
        delta: GraphMode.delta,
      },
    };
  },
  mounted() {
    this.updateValue();
  },
  computed: {
    /**
     * @return Whether the project is currently in delta view.
     */
    inDeltaView(): boolean {
      return deltaStore.inDeltaView;
    },
    /**
     * @return Whether the tree view is disabled.
     */
    isTreeDisabled(): boolean {
      return documentStore.isTableOnlyDocument;
    },
    /**
     * @return Whether the tree view is disabled.
     */
    isDeltaDisabled(): boolean {
      return layoutStore.mode === GraphMode.tim;
    },
  },
  methods: {
    /**
     * Updates the values of which buttons are highlighted.
     */
    updateValue(): void {
      const selected: GraphMode[] = [];

      selected.push(layoutStore.mode);

      if (this.inDeltaView) {
        selected.push(GraphMode.delta);
      }

      this.value = selected;
    },
    /**
     * Opens tree view.
     */
    handleTimView(): void {
      layoutStore.mode = GraphMode.tim;
      this.updateValue();
    },
    /**
     * Opens tree view.
     */
    handleTreeView(): void {
      layoutStore.mode = GraphMode.tree;
      this.updateValue();
    },
    /**
     * Opens table view.
     */
    handleTableView(): void {
      layoutStore.mode = GraphMode.table;
      this.updateValue();
    },
    /**
     * Opens delta view.
     */
    handleDeltaView(): void {
      appStore.openDetailsPanel("delta");
      this.updateValue();
    },
  },
  watch: {
    /**
     * Updates the value when delta view changes.
     */
    inDeltaView(): void {
      this.updateValue();
    },
    /**
     * Updates the value when the document type changes.
     */
    isTreeDisabled(): void {
      this.updateValue();
    },
    /**
     * Updates the value when the graph mode changes.
     */
    isDeltaDisabled(): void {
      this.updateValue();
    },
  },
});
</script>
