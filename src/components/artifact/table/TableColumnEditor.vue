<template>
  <v-select
    ref="tableColumnEditor"
    v-model="select"
    :items="items"
    :label="selectDisplay"
    outlined
    dense
    hide-details
    style="width: 200px"
    @focus="handleLoadItems"
  >
    <template v-slot:selection> {{ selectDisplay }} </template>
    <template v-slot:item="{ item }">
      <v-row dense align="center">
        <v-col @click.stop="handleEditOpen(item)">
          {{ item.name }}
        </v-col>
        <v-col @click.stop="" style="flex-grow: 0.5">
          <generic-icon-button
            :is-disabled="isFirstItem(item)"
            icon-id="mdi-arrow-up"
            :tooltip="`Move '${item.name}' Up`"
            @click="handleMove(item, true)"
          />
          <generic-icon-button
            :is-disabled="isLastItem(item)"
            icon-id="mdi-arrow-down"
            :tooltip="`Move '${item.name}' Down`"
            @click="handleMove(item, false)"
          />
        </v-col>
      </v-row>
    </template>

    <template v-slot:append-item>
      <v-btn text block color="primary" @click="handleCreateOpen">
        <v-icon>mdi-plus</v-icon>
        Add Column
      </v-btn>

      <table-column-modal :is-open="isCreateOpen" @close="handleCloseModal" />

      <table-column-modal
        :is-open="isEditOpen"
        :column="editingColumn"
        @close="handleCloseModal"
      />
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentColumn } from "@/types";
import { columnTypeOptions } from "@/util";
import { documentModule } from "@/store";
import { handleColumnMove } from "@/api";
import { GenericIconButton } from "@/components/common";
import TableColumnModal from "./TableColumnModal.vue";

export default Vue.extend({
  name: "TableColumnEditor",
  components: { TableColumnModal, GenericIconButton },
  data() {
    return {
      isCreateOpen: false,
      isEditOpen: false,
      editingColumn: undefined as DocumentColumn | undefined,
      items: documentModule.tableColumns,
      dataTypes: columnTypeOptions(),
    };
  },
  computed: {
    /**
     * @return The select display name.
     */
    selectDisplay(): string {
      return `${documentModule.tableColumns.length} Columns`;
    },
    /**
     * Emulates a select value to open the column editor on click.
     */
    select: {
      get() {
        return undefined;
      },
      set(column?: DocumentColumn) {
        if (!column) return;
        this.handleEditOpen(column);
      },
    },
  },
  methods: {
    /**
     * Resets modal data and closes all modals.
     */
    handleCloseModal() {
      (this.$refs.tableColumnEditor as HTMLElement).blur();
      this.isCreateOpen = false;
      this.isEditOpen = false;
      this.editingColumn = undefined;
    },
    /**
     * Opens the create modal.
     */
    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    /**
     * Opens the edit modal.
     * @param column - The column to edit.
     */
    handleEditOpen(column: DocumentColumn) {
      this.editingColumn = column;
      this.isEditOpen = true;
    },

    /**
     * Returns whether the given column is the first.
     * @param item - The column to check.
     * @return Whether it is first.
     */
    isFirstItem(item: DocumentColumn) {
      return this.items.indexOf(item) === 0;
    },
    /**
     * Returns whether the given column is the last.
     * @param item - The column to check.
     * @return Whether it is last.
     */
    isLastItem(item: DocumentColumn) {
      return this.items.indexOf(item) === this.items.length - 1;
    },

    /**
     * Loads the current table columns.
     */
    handleLoadItems() {
      this.items = documentModule.tableColumns;
    },
    /**
     * Changes the order of two columns.
     * @param item - The column to move.
     * @param moveUp - Whether to move the column up or down.
     */
    handleMove(item: DocumentColumn, moveUp: boolean) {
      handleColumnMove(item, moveUp, {
        onSuccess: (columns) => (this.items = columns),
      });
    },
  },
});
</script>
