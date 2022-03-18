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
import { DocumentColumn, SelectOption } from "@/types";
import { documentModule, logModule } from "@/store";
import { GenericModal } from "@/components/common/generic";
import { columnTypeOptions, createColumn } from "@/util";
import { editDocument } from "@/api";

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
      type: Object as PropType<DocumentColumn>,
      required: false,
    },
  },
  data() {
    return {
      editingColumn: createColumn(this.column),
      confirmDelete: false,
    };
  },
  computed: {
    isEditMode(): boolean {
      return !!this.column;
    },
    title(): string {
      return this.isEditMode ? "Edit Column" : "Add Column";
    },
    dataTypes(): SelectOption[] {
      return columnTypeOptions();
    },

    isNameValid(): boolean {
      return (
        !documentModule.doesColumnExist(this.editingColumn.name) ||
        this.column?.name === this.editingColumn.name
      );
    },
    isColumnValid(): boolean {
      return !!this.editingColumn.name && this.isNameValid;
    },
    nameErrors(): string[] {
      return this.isNameValid ? [] : ["This name already exists"];
    },
  },
  methods: {
    resetModalData() {
      this.editingColumn = createColumn(this.column);
      this.confirmDelete = false;
      this.$emit("close");
    },
    handleSubmit() {
      const document = documentModule.document;

      if (!this.isEditMode) {
        document.columns = [...(document.columns || []), this.editingColumn];
      }

      editDocument(document)
        .then(() => {
          logModule.onSuccess(`Column updated: ${this.editingColumn.name}`);
          this.resetModalData();
        })
        .catch(() => {
          logModule.onError(
            `Unable to update column: ${this.editingColumn.name}`
          );
        });
    },
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        const document = documentModule.document;

        document.columns = (document.columns || []).filter(
          ({ id }) => id === this.editingColumn.id
        );

        editDocument(document)
          .then(() => {
            logModule.onSuccess(`Column deleted: ${this.editingColumn.name}`);
            this.resetModalData();
          })
          .catch(() => {
            logModule.onError(
              `Unable to deleted column: ${this.editingColumn.name}`
            );
          });
      }
    },
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.editingColumn = createColumn(this.column);
    },
  },
});
</script>
