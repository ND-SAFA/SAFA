<template>
  <generic-modal
    :title="modalTitle"
    size="sm"
    :is-open="isOpen"
    @close="handleClose"
  >
    <template v-slot:body>
      <v-text-field
        filled
        label="Name"
        class="mt-4"
        v-model="editedColumn.name"
        :error-messages="nameErrors"
      />
      <v-select
        filled
        label="Type"
        :items="dataTypes"
        v-model="editedColumn.dataType"
        item-text="name"
        item-value="id"
      />
      <v-checkbox
        label="Requires a non-empty value"
        v-model="editedColumn.required"
      />
    </template>
    <template v-slot:actions>
      <v-btn
        v-if="isEditMode"
        color="error"
        :text="!confirmDelete"
        :outlined="confirmDelete"
        @click="handleDelete"
      >
        {{ confirmDelete ? "Delete" : "Delete Column" }}
      </v-btn>
      <v-btn outlined v-if="confirmDelete" @click="confirmDelete = false">
        Cancel
      </v-btn>
      <v-spacer />
      <v-btn color="primary" :disabled="!canSave" @click="handleSubmit">
        Confirm
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { ColumnModel } from "@/types";
import { columnTypeOptions } from "@/util";
import { tableColumnSaveStore } from "@/hooks";
import { handleColumnDelete, handleColumnSave } from "@/api";
import { GenericModal } from "@/components/common";

/**
 * Represents a modal for editing a table column.
 *
 * @emits-1 `close` - On close.
 */
export default Vue.extend({
  name: "TableColumnModal",
  components: { GenericModal },
  props: {
    isOpen: Boolean,
  },
  data() {
    return {
      confirmDelete: false,
      dataTypes: columnTypeOptions(),
    };
  },
  computed: {
    /**
     * @return Whether an existing column is being updated.
     */
    isUpdate(): boolean {
      return tableColumnSaveStore.isUpdate;
    },
    /**
     * @return The column being edited
     */
    editedColumn(): ColumnModel {
      return tableColumnSaveStore.editedColumn;
    },
    /**
     * @return The modal title.
     */
    modalTitle(): string {
      return this.isUpdate ? "Edit Column" : "Add Column";
    },
    /**
     * @return Whether the column can be saved.
     */
    canSave(): boolean {
      return tableColumnSaveStore.canSave;
    },
    /**
     * @return Any errors to report on the name.
     */
    nameErrors(): string[] {
      return tableColumnSaveStore.editedColumn.name === ""
        ? []
        : tableColumnSaveStore.nameErrors;
    },
  },
  methods: {
    /**
     * Resets modal data and closes the modal.
     */
    handleClose() {
      this.$emit("close");
    },
    /**
     * Attempts to save a column.
     */
    handleSubmit() {
      handleColumnSave({
        onSuccess: () => this.handleClose(),
      });
    },
    /**
     * Attempts to delete an existing column.
     */
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        handleColumnDelete({
          onSuccess: () => this.handleClose(),
        });
      }
    },
  },
  watch: {
    /**
     * When opened, the modal will reset the column being edited.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.confirmDelete = false;
      tableColumnSaveStore.resetColumn();
    },
  },
});
</script>
