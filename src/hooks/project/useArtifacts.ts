import { defineStore } from "pinia";

import { pinia } from "@/plugins";

/**
 * This module defines the state of the current project's artifacts.
 */
export const useArtifacts = defineStore("artifacts", {
  state: () => ({}),
  getters: {},
  actions: {},
});

export default useArtifacts(pinia);
