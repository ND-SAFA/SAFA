import { defineStore } from "pinia";

import { buildOrg } from "@/util";
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
  }),
  getters: {
    /**
     * @return The current organization id.
     */
    orgId(): string {
      return this.org.id;
    },
  },
  actions: {},
});

export default useOrg(pinia);
