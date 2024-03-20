import { defineStore } from "pinia";

import { OrganizationSchema, TransactionSchema } from "@/types";
import { buildOrg, removeMatches } from "@/util";
import { membersStore, teamStore } from "@/hooks";
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
    /**
     * All transactions that the org has made.
     */
    allTransactions: [] as TransactionSchema[],
    /**
     * All transactions that the org has made in the last month.
     */
    monthlyTransactions: [] as TransactionSchema[],
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
        this.org.billing.paymentTier === "UNLIMITED" ||
        this.org.billing.paymentTier === "RECURRING"
      );
    },
  },
  actions: {
    /**
     * Initializes an organization.
     * @param org - The organization to initialize.
     */
    initialize(org: OrganizationSchema): void {
      this.org = org;

      this.addOrg(org);
      membersStore.initialize(org.members, "ORGANIZATION");
      teamStore.initializeOrg(org);
    },
    /**
     * Synchronizes loaded data for the current organization.
     */
    sync(
      allTransactions: TransactionSchema[],
      monthlyTransactions: TransactionSchema[]
    ): void {
      this.allTransactions = allTransactions;
      this.monthlyTransactions = monthlyTransactions;
    },
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
     * @param onCurrentRemoved - The callback to call if the current organization is removed.
     */
    removeOrg(
      org: OrganizationSchema,
      onCurrentRemoved?: (newOrg: OrganizationSchema) => void
    ): void {
      this.allOrgs = removeMatches(this.allOrgs, "id", [org.id]);

      if (org.id === this.org.id) {
        this.org = this.allOrgs[0] || buildOrg();
        onCurrentRemoved?.(this.org);
      }
    },
  },
});

export default useOrg(pinia);
