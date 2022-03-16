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

      <generic-modal
        title="Add Column"
        size="sm"
        :is-open="isCreateOpen"
        @close="resetModalData"
      >
        <template v-slot:body>
          <v-text-field
            filled
            label="Name"
            class="mt-4"
            v-model="columnName"
            :error-messages="nameErrors"
          />
          <v-select
            filled
            label="Type"
            :items="dataTypes"
            v-model="columnType"
            item-text="name"
            item-value="id"
          />
        </template>
        <template v-slot:actions>
          <v-spacer />
          <v-btn
            color="primary"
            :disabled="!isColumnValid"
            @click="handleAddColumn"
          >
            Create Column
          </v-btn>
        </template>
      </generic-modal>

      <generic-modal
        title="Edit Column"
        size="sm"
        :is-open="isEditOpen"
        @close="resetModalData"
      >
        <template v-slot:body>
          <v-text-field
            filled
            label="Name"
            class="mt-4"
            v-model="columnName"
            :error-messages="nameErrors"
          />
          <v-select
            filled
            label="Type"
            :items="dataTypes"
            v-model="columnType"
            item-text="name"
            item-value="id"
          />
        </template>
        <template v-slot:actions>
          <v-btn
            color="error"
            :text="!confirmDelete"
            :outlined="confirmDelete"
            @click="handleDeleteColumn"
          >
            {{ confirmDelete ? "Delete" : "Delete Column" }}
          </v-btn>
          <v-btn outlined v-if="confirmDelete" @click="confirmDelete = false">
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            :disabled="!isColumnValid"
            @click="handleEditColumn"
          >
            Confirm Edit
          </v-btn>
        </template>
      </generic-modal>
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import { ColumnDataType, DocumentColumn, SelectOption } from "@/types";
import { documentModule } from "@/store";
import { GenericIconButton, GenericModal } from "@/components/common/generic";
import { columnTypeOptions } from "@/util";

export default Vue.extend({
  name: "TableColumnEditor",
  components: { GenericModal, GenericIconButton },
  data: () => ({
    isCreateOpen: false,
    isEditOpen: false,
    editingColumn: undefined as DocumentColumn | undefined,
    confirmDelete: false,
    columnName: "",
    columnType: ColumnDataType.FREE_TEXT,
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

    isNameValid(): boolean {
      return (
        !documentModule.doesColumnExist(this.columnName) ||
        this.editingColumn?.name === this.columnName
      );
    },
    isColumnValid(): boolean {
      return !!this.columnName && this.isNameValid;
    },
    nameErrors(): string[] {
      return this.isNameValid ? [] : ["This name already exists"];
    },
  },
  methods: {
    handleCloseMenu() {
      (this.$refs.tableColumnEditor as HTMLElement).blur();
    },
    resetModalData() {
      this.columnName = "";
      this.columnType = ColumnDataType.FREE_TEXT;
      this.editingColumn = undefined;
      this.isCreateOpen = false;
      this.isEditOpen = false;
      this.confirmDelete = false;
      this.handleCloseMenu();
    },

    handleCreateOpen() {
      this.isCreateOpen = true;
    },
    handleAddColumn() {
      // TODO: add new column to document.
      // addNewDocument(this.documentName, this.documentType, this.artifactIds)
      //   .then(() => {
      //     logModule.onSuccess(`Document created: ${this.documentName}`);
      //     this.resetModalData();
      //   })
      //   .catch(() => {
      //     logModule.onError(`Unable to create document: ${this.documentName}`);
      //   });
    },

    handleEditOpen(column: DocumentColumn) {
      this.editingColumn = column;
      this.columnName = column.name;
      this.columnType = column.dataType;
      this.isEditOpen = true;
    },
    handleEditColumn() {
      if (this.editingColumn) {
        this.editingColumn.name = this.columnName;
        this.editingColumn.dataType = this.columnType;

        // TODO: edit document columns
        // editDocument(this.editingDocument)
        //   .then(() => {
        //     logModule.onSuccess(`Document edited: ${this.documentName}`);
        //     this.resetModalData();
        //   })
        //   .catch(() => {
        //     logModule.onError(`Unable to edit document: ${this.documentName}`);
        //   });
      }
    },
    handleDeleteColumn() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else if (this.editingColumn) {
        // TODO: delete the current column.
        // deleteAndSwitchDocuments(this.editingDocument)
        //   .then(() => {
        //     logModule.onSuccess(`Document Deleted: ${this.documentName}`);
        //     this.resetModalData();
        //   })
        //   .catch(() => {
        //     logModule.onError(
        //       `Unable to delete document: ${this.documentName}`
        //     );
        //   });
      }
    },
  },
});
</script>

<style lang="scss">
.v-list-item--active {
  color: white !important;
}
</style>
