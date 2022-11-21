<template>
  <v-btn-toggle tile group multiple dense :value="value">
    <v-btn
      value="tree"
      text
      color="accent"
      data-cy="button-nav-tree"
      @click="handleTreeView"
    >
      <v-icon left color="accent">mdi-family-tree</v-icon>
      Tree
    </v-btn>
    <v-btn
      value="table"
      text
      color="accent"
      data-cy="button-nav-table"
      @click="handleTableView"
    >
      <v-icon left color="accent">mdi-table-multiple</v-icon>
      Table
    </v-btn>
    <v-btn
      value="delta"
      text
      color="accent"
      data-cy="button-nav-delta"
      @click="handleDeltaView"
    >
      <v-icon left color="accent">mdi-compare</v-icon>
      Delta
    </v-btn>
  </v-btn-toggle>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore, deltaStore, documentStore } from "@/hooks";

/**
 * Buttons for changing the mode of the artifact view.
 */
export default Vue.extend({
  name: "ModeButtons",
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
  },
  methods: {
    /**
     * Updates the values of which buttons are highlighted.
     */
    updateValue(): void {
      const selected: string[] = [];

      selected.push(documentStore.isTableView ? "table" : "tree");

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
  },
});
</script>

<style scoped lang="scss"></style>
