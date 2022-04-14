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

      <table-column-modal :is-open="isCreateOpen" @close="handleCloseMenu" />

      <table-column-modal
        :is-open="isEditOpen"
        :column="editingColumn"
        @close="handleCloseMenu"
      />
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentColumn, SelectOption } from "@/types";
import { documentModule, logModule } from "@/store";
import { GenericIconButton } from "@/components/common/generic";
import { columnTypeOptions } from "@/util";
import TableColumnModal from "./TableColumnModal.vue";
import { handleUpdateDocument } from "@/api";

export default Vue.extend({
  name: "TableColumnEditor",
  components: { TableColumnModal, GenericIconButton },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    editingColumn: undefined as DocumentColumn | undefined,
    items: documentModule.tableColumns,
  }),
  computed: {
    dataTypes(): SelectOption[] {
      return columnTypeOptions();
    },
    selectDisplay(): string {
      return `${documentModule.tableColumns.length} Columns`;
    },
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
    handleCloseMenu() {
      (this.$refs.tableColumnEditor as HTMLElement).blur();
      this.isCreateOpen = false;
      this.isEditOpen = false;
      this.editingColumn = undefined;
    },
    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    handleEditOpen(column: DocumentColumn) {
      this.editingColumn = column;
      this.isEditOpen = true;
    },
    isFirstItem(item: DocumentColumn) {
      return this.items.indexOf(item) === 0;
    },
    isLastItem(item: DocumentColumn) {
      return this.items.indexOf(item) === this.items.length - 1;
    },
    handleLoadItems() {
      this.items = documentModule.tableColumns;
    },
    handleMove(item: DocumentColumn, moveUp: boolean) {
      const currentIndex = this.items.indexOf(item);
      const swapIndex = moveUp ? currentIndex - 1 : currentIndex + 1;
      const document = documentModule.document;
      const columns = document.columns || [];

      [columns[currentIndex], columns[swapIndex]] = [
        columns[swapIndex],
        columns[currentIndex],
      ];

      this.items = document.columns = [...columns];

      handleUpdateDocument(document)
        .then(() => {
          logModule.onSuccess(`Column order updated`);
        })
        .catch(() => {
          logModule.onError(`Unable to update column order`);
        });
    },
  },
});
</script>
