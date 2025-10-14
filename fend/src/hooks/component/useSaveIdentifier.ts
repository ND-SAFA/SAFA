import { defineStore } from "pinia";

import { IdentifierSchema, PopupType } from "@/types";
import { buildProjectIdentifier } from "@/util";
import { appStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * The save identifier store assists in creating and editing project identifiers.
 */
export const useSaveIdentifier = defineStore("saveIdentifier", {
  state: () => ({
    /**
     * A base identifier being edited.
     */
    baseIdentifier: undefined as IdentifierSchema | undefined,
    /**
     * The identifier being created or edited.
     */
    editedIdentifier: buildProjectIdentifier(),
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
      return this.editedIdentifier.name.trim().length > 0;
    },
  },
  actions: {
    /**
     * Resets the identifier value to the given base value.
     * @param clear - Whether to clear the base identifier.
     */
    resetIdentifier(clear?: boolean): void {
      if (clear) {
        this.baseIdentifier = undefined;
      }

      this.editedIdentifier = buildProjectIdentifier(this.baseIdentifier);
    },
    /**
     * Selects an identifier and opens the edit or delete modal.
     *
     * @param identifier - The identifier to select.
     * @param mode - The type of action to open a modal for.
     */
    selectIdentifier(
      identifier: IdentifierSchema | undefined,
      mode: "save" | "edit" | "delete" | "transfer"
    ): void {
      this.baseIdentifier = identifier;
      this.resetIdentifier();

      const panelName = (
        {
          save: "saveProject",
          edit: "editProject",
          delete: "deleteProject",
          transfer: "moveProject",
        } as Record<"save" | "edit" | "delete" | "transfer", PopupType>
      )[mode];

      appStore.open(panelName);
    },
  },
});

export default useSaveIdentifier(pinia);
