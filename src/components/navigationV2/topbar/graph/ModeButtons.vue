<template>
  <v-btn-toggle tile group multiple dense :value="value">
    <v-btn text color="accent" @click="handleTreeView">
      <v-icon left color="accent">mdi-family-tree</v-icon>
      Tree
    </v-btn>
    <v-btn text color="accent" @click="handleTableView">
      <v-icon left color="accent">mdi-table-multiple</v-icon>
      Table
    </v-btn>
    <v-btn text color="accent" @click="handleDeltaView">
      <v-icon left color="accent">mdi-compare</v-icon>
      Delta
    </v-btn>
  </v-btn-toggle>
</template>

<script lang="ts">
import Vue from "vue";
import { deltaStore, documentStore } from "@/hooks";

/**
 * Buttons for changing the mode of the artifact view.
 */
export default Vue.extend({
  name: "ModeButtons",
  components: {},
  props: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return The indexes of which buttons are highlighted.
     */
    value(): number[] {
      const indexes: number[] = [];

      indexes.push(documentStore.isTableView ? 1 : 0);

      if (deltaStore.inDeltaView) {
        indexes.push(2);
      }

      return indexes;
    },
  },
  methods: {
    /**
     * Opens tree view.
     */
    handleTreeView(): void {
      documentStore.isTableView = false;
    },
    /**
     * Opens table view.
     */
    handleTableView(): void {
      documentStore.isTableView = true;
    },
    /**
     * Opens delta view.
     */
    handleDeltaView(): void {
      //TODO
    },
  },
});
</script>

<style scoped lang="scss"></style>
