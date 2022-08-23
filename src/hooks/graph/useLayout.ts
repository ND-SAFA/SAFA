import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  ArtifactPositions,
  IGraphLayout,
  LayoutPayload,
  LayoutPosition,
} from "@/types";
import {
  ArtifactGraphLayout,
  artifactTreeCyPromise,
  cyApplyAutomove,
  cyCreateLayout,
  cyResetTim,
  cyResetTree,
  TimGraphLayout,
  timTreeCyPromise,
} from "@/cytoscape";
import { appStore } from "@/hooks/core";

/**
 * This module handles the layout positions of the graph.
 */
export const useLayout = defineStore("layout", {
  state: () => ({
    /**
     * A mapping from artifact ID to its position.
     */
    artifactPositions: {} as ArtifactPositions,
    /**
     * The current graph layout.
     */
    layout: undefined as IGraphLayout | undefined,
  }),
  getters: {},
  actions: {
    /**
     * Returns the position of an artifact.
     *
     * @param artifactId - The artifact id to find.
     * @return Its position.
     */
    getArtifactPosition(artifactId: string): LayoutPosition {
      return this.artifactPositions[artifactId] || { x: 0, y: 0 };
    },
    /**
     * Resets all automove events.
     */
    applyAutomove(): void {
      if (!this.layout) return;

      cyApplyAutomove(this.layout);
    },
    /**
     * Resets the graph layout.
     */
    setGraphLayout(layoutPayload: LayoutPayload): void {
      appStore.onLoadStart();

      this.layout = layoutPayload.layout;
      cyCreateLayout(layoutPayload);
      this.applyAutomove();

      setTimeout(() => {
        appStore.onLoadEnd();
        cyResetTim();
        cyResetTree();
      }, 200);
    },
    /**
     * Resets the graph layout of the artifact tree.
     */
    setArtifactTreeLayout(): void {
      const layout = new ArtifactGraphLayout();
      const payload = { layout, cyPromise: artifactTreeCyPromise };

      this.setGraphLayout(payload);
    },
    /**
     * Resets the graph layout of the TIM tree.
     */
    setTimTreeLayout(): void {
      const layout = new TimGraphLayout();
      const payload = { layout, cyPromise: timTreeCyPromise };

      this.setGraphLayout(payload);
    },
  },
});

export default useLayout(pinia);
