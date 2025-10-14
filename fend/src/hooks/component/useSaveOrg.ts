import { defineStore } from "pinia";

import { OrganizationSchema } from "@/types";
import { buildOrg } from "@/util";
import { pinia } from "@/plugins";

/**
 * The save organization store assists in creating and editing organizations.
 */
export const useSaveOrg = defineStore("saveOrg", {
  state: () => ({
    /**
     * A base organization being edited.
     */
    baseOrg: undefined as OrganizationSchema | undefined,
    /**
     * The organization being created or edited.
     */
    editedOrg: buildOrg(),
  }),
  getters: {
    /**
     * @return Whether an existing organization is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseOrg;
    },
    /**
     * @return Whether the organization can be saved.
     */
    canSave(): boolean {
      return this.editedOrg.name.length > 0;
    },
  },
  actions: {
    /**
     * Resets the organization value to the given base value.
     */
    resetOrg(org?: OrganizationSchema): void {
      if (org) {
        this.baseOrg = org;
      }

      this.editedOrg = buildOrg(this.baseOrg);
    },
  },
});

export default useSaveOrg(pinia);
