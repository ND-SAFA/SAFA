import { defineStore } from "pinia";

import { IdentifierModel } from "@/types";
import { createProjectIdentifier } from "@/util";
import { pinia } from "@/plugins";

/**
 * The save identifier store assists in creating and editing project identifiers.
 */
export const useSaveIdentifier = defineStore("saveIdentifier", {
  state: () => ({
    /**
     * A base identifier being edited.
     */
    baseIdentifier: undefined as IdentifierModel | undefined,
    /**
     * The identifier being created or edited.
     */
    editedIdentifier: createProjectIdentifier(),
  }),
  getters: {
    /**
     * @return Whether an existing identifier is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseIdentifier;
    },
    /**
     * @return Whether the identifier can be saved.
     */
    canSave(): boolean {
      return this.editedIdentifier.name.length > 0;
    },
  },
  actions: {
    /**
     * Resets the identifier value to the given base value.
     */
    resetIdentifier(): void {
      this.editedIdentifier = createProjectIdentifier(this.baseIdentifier);
    },
  },
});

export default useSaveIdentifier(pinia);
