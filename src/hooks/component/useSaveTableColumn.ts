import { defineStore } from "pinia";

import { ColumnModel } from "@/types";
import { createColumn } from "@/util";
import { pinia } from "@/plugins";
import documentStore from "../project/useDocuments";

/**
 * The save column store assists in creating and editing document columns.
 */
export const useSaveTableColumn = defineStore("saveTableColumn", {
  state: () => ({
    /**
     * A base column being edited.
     */
    baseColumn: undefined as ColumnModel | undefined,
    /**
     * The column being created or edited.
     */
    editedColumn: createColumn(),
  }),
  getters: {
    /**
     * @return Whether an existing column is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseColumn;
    },
    /**
     * @return Whether the current name is valid.
     */
    isNameValid(): boolean {
      return (
        !documentStore.doesColumnExist(this.editedColumn.name) ||
        this.baseColumn?.name === this.editedColumn.name
      );
    },
    /**
     * @return Any errors to report on the name.
     */
    nameErrors(): string[] {
      return this.isNameValid
        ? []
        : ["This name is already used, please select another."];
    },
    /**
     * @return Whether the column can be saved.
     */
    canSave(): boolean {
      return this.editedColumn.name.length > 0 && this.isNameValid;
    },
  },
  actions: {
    /**
     * Resets the column value to the given base value.
     */
    resetColumn(): void {
      this.editedColumn = createColumn(this.baseColumn);
    },
  },
});

export default useSaveTableColumn(pinia);
