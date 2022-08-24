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
  disableDrawMode,
  TimGraphLayout,
  timTreeCyPromise,
} from "@/cytoscape";
import { appStore } from "@/hooks/core";
import selectionStore from "@/hooks/graph/useSelection";
import subtreeStore from "@/hooks/project/useSubtree";
import deltaStore from "@/hooks/project/useDelta";

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
     * A saved position for a node to be added.
     */
    savedPosition: undefined as LayoutPosition | undefined,
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
     * Sets the position of an artifact to the saved one, and clears the saved position.
     *
     * @param artifactId - The artifact id to set.
     */
    setArtifactToSavedPosition(artifactId: string): void {
      if (!this.savedPosition) return;

      this.$patch({
        savedPosition: undefined,
        artifactPositions: {
          ...this.artifactPositions,
          [artifactId]: this.savedPosition,
        },
      });
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
    /**
     * Resets the layout of the graph.
     */
    async resetLayout(): Promise<void> {
      appStore.onLoadStart();

      disableDrawMode();
      subtreeStore.resetHiddenNodes();
      selectionStore.clearSelections();
      deltaStore.clear();
      appStore.closeSidePanels();

      setTimeout(() => {
        this.setArtifactTreeLayout();
        appStore.onLoadEnd();
      }, 200);
    },
    /**
     * Updates artifact positions and resets the layout.
     *
     * @param positions - The new positions to set.
     */
    async updatePositions(positions: ArtifactPositions): Promise<void> {
      this.artifactPositions = positions;

      await this.resetLayout();
    },
  },
});

export default useLayout(pinia);
