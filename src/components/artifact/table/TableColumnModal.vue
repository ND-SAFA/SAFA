<template>
  <generic-modal
    :title="title"
    size="sm"
    :is-open="isOpen"
    @close="resetModalData"
  >
    <template v-slot:body>
      <v-text-field
        filled
        label="Name"
        class="mt-4"
        v-model="editingColumn.name"
        :error-messages="nameErrors"
      />
      <v-select
        filled
        label="Type"
        :items="dataTypes"
        v-model="editingColumn.dataType"
        item-text="name"
        item-value="id"
      />
      <v-checkbox
        label="Requires a non-empty value"
        v-model="editingColumn.required"
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
      <v-btn color="primary" :disabled="!isColumnValid" @click="handleSubmit">
        Confirm
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ColumnModel } from "@/types";
import { columnTypeOptions, createColumn } from "@/util";
import { documentModule } from "@/store";
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
    column: {
      type: Object as PropType<ColumnModel>,
      required: false,
    },
  },
  data() {
    return {
      editingColumn: createColumn(this.column),
      confirmDelete: false,
      dataTypes: columnTypeOptions(),
    };
  },
  computed: {
    /**
     * @return Whether the modal is in edit mode.
     */
    isEditMode(): boolean {
      return !!this.column;
    },
    /**
     * @return The modal title.
     */
    title(): string {
      return this.isEditMode ? "Edit Column" : "Add Column";
    },

    /**
     * @return Whether the current name is valid.
     */
    isNameValid(): boolean {
      return (
        !documentModule.doesColumnExist(this.editingColumn.name) ||
        this.column?.name === this.editingColumn.name
      );
    },
    /**
     * @return Whether the current column is valid.
     */
    isColumnValid(): boolean {
      return !!this.editingColumn.name && this.isNameValid;
    },
    /**
     * @return Any errors to report on the name.
     */
    nameErrors(): string[] {
      return this.isNameValid ? [] : ["This name already exists"];
    },
  },
  methods: {
    /**
     * Resets modal data and closes the modal.
     */
    resetModalData() {
      this.editingColumn = createColumn(this.column);
      this.confirmDelete = false;
      this.$emit("close");
    },
    /**
     * Attempts to save a column.
     */
    handleSubmit() {
      handleColumnSave(this.editingColumn, this.isEditMode, {
        onSuccess: () => this.resetModalData(),
      });
    },
    /**
     * Attempts to delete an existing column.
     */
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        handleColumnDelete(this.editingColumn, {
          onSuccess: () => this.resetModalData(),
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

      this.editingColumn = createColumn(this.column);
    },
  },
});
</script>
