import { defineStore } from "pinia";

import { OrganizationSchema } from "@/types";
import { buildOrg, removeMatches } from "@/util";
import { pinia } from "@/plugins";

/**
 * A store for managing the state of the user's current organization.
 */
export const useOrg = defineStore("org", {
  state: () => ({
    /**
     * The currently loaded organization.
     */
    org: buildOrg(),
    /**
     * All organizations the user has access to.
     */
    allOrgs: [] as OrganizationSchema[],
  }),
  getters: {
    /**
     * @return All orgs that have not been loaded.
     */
    unloadedOrgs(): OrganizationSchema[] {
      return this.allOrgs.filter(({ id }) => id !== this.orgId);
    },
    /**
     * @return The current organization id.
     */
    orgId(): string {
      return this.org.id;
    },
    /**
     * @return Whether this org has automatic billing, and does not need to see as-needed billing details.
     */
    automaticBilling(): boolean {
      return (
        this.org.paymentTier === "UNLIMITED" ||
        this.org.paymentTier === "RECURRING"
      );
    },
  },
  actions: {
    /**
     * Adds an organization to the list of all organizations.
     * @param org - The organization to add.
     */
    addOrg(org: OrganizationSchema): void {
      this.allOrgs = [org, ...removeMatches(this.allOrgs, "id", [org.id])];
    },
    /**
     * Removes an organization to the list of all organizations.
     * - If the organization is the current organization,
     *   the first organization in the list will be set as the current.
     * @param org - The organization to remove.
     */
    removeOrg(org: OrganizationSchema): void {
      this.allOrgs = removeMatches(this.allOrgs, "id", [org.id]);

      if (org.id === this.org.id) {
        this.org = this.allOrgs[0] || buildOrg();
      }
    },
  },
});

export default useOrg(pinia);
