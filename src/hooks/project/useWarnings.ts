import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import { ProjectWarnings } from "@/types";

/**
 * This module defines the state of warnings generated for
 * artifacts in this version.
 */
export const useWarnings = defineStore("warnings", {
  state: () => ({
    /**
     * A collection of warnings keyed by the associated artifact.
     */
    artifactWarnings: {} as ProjectWarnings,
  }),
  getters: {},
  actions: {
    /**
     * Returns all warnings for the given artifacts.
     *
     * @param artifactIds - The ids of artifacts to get warnings for.
     * @return All warnings.
     */
    getArtifactWarnings(artifactIds: string[]) {
      return artifactIds
        .map((id) => this.artifactWarnings[id] || [])
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
  },
});

export default useWarnings(pinia);
