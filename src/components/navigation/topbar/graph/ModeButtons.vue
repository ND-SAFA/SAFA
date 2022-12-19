<template>
  <v-btn-toggle tile group multiple dense :value="value">
    <text-button
      :disabled="isTreeDisabled"
      value="tree"
      text
      color="accent"
      data-cy="button-nav-tree"
      icon-id="mdi-family-tree"
      @click="handleTreeView"
    >
      Tree
    </text-button>
    <text-button
      value="table"
      text
      color="accent"
      data-cy="button-nav-table"
      icon-id="mdi-table-multiple"
      @click="handleTableView"
    >
      Table
    </text-button>
    <text-button
      value="delta"
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
import { appStore, deltaStore, documentStore } from "@/hooks";
import { TextButton } from "@/components/common";

/**
 * Buttons for changing the mode of the artifact view.
 */
export default Vue.extend({
  name: "ModeButtons",
  components: { TextButton },
  data() {
    return {
      value: [] as string[],
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
      return documentStore.isEditableTableDocument;
    },
  },
  methods: {
    /**
     * Updates the values of which buttons are highlighted.
     */
    updateValue(): void {
      const selected: string[] = [];

      selected.push(documentStore.isTableDocument ? "table" : "tree");

      if (this.inDeltaView) {
        selected.push("delta");
      }

      this.value = selected;
    },
    /**
     * Opens tree view.
     */
    handleTreeView(): void {
      documentStore.isTableView = false;
      this.updateValue();
    },
    /**
     * Opens table view.
     */
    handleTableView(): void {
      documentStore.isTableView = true;
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
  },
});
</script>

<style scoped lang="scss"></style>
