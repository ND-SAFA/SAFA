import { defineStore } from "pinia";

import { IdentifierSchema, PanelType } from "@/types";
import { createProjectIdentifier } from "@/util";
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
    /**
     * Selects an identifier and opens the edit or delete modal.
     *
     * @param identifier - The identifier to select.
     * @param mode - The type of action to open a modal for.
     */
    selectIdentifier(
      identifier: IdentifierSchema | undefined,
      mode: "save" | "edit" | "delete"
    ): void {
      this.baseIdentifier = identifier;
      this.resetIdentifier();

      const panelName = (
        {
          save: "projectSaver",
          edit: "projectEditor",
          delete: "projectDeleter",
        } as Record<"save" | "edit" | "delete", PanelType>
      )[mode];

      appStore.isOpen[panelName] = true;
    },
  },
});

export default useSaveIdentifier(pinia);
