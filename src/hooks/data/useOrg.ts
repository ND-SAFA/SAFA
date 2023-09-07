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
  getters: {},
  actions: {},
});

export default useOrg(pinia);
