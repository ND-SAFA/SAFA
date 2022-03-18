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
  >
    <template v-slot:selection> {{ selectDisplay }} </template>
    <template v-slot:item="{ item }">
      <v-row dense align="center" @click.stop="handleEditOpen(item)">
        <v-col>
          {{ item.name }}
        </v-col>
        <v-col class="flex-grow-0">
          <generic-icon-button
            v-if="item.name !== 'Default'"
            icon-id="mdi-dots-horizontal"
            :tooltip="`Edit ${item.name}`"
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
import { documentModule } from "@/store";
import { GenericIconButton } from "@/components/common/generic";
import { columnTypeOptions } from "@/util";
import TableColumnModal from "./TableColumnModal.vue";

export default Vue.extend({
  name: "TableColumnEditor",
  components: { TableColumnModal, GenericIconButton },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    editingColumn: undefined as DocumentColumn | undefined,
  }),
  computed: {
    items(): DocumentColumn[] {
      return documentModule.tableColumns;
    },
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
  },
});
</script>
