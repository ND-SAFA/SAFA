import { defineStore } from "pinia";

import { LayoutOptions, NodeSingular } from "cytoscape";
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
import { documentStore, projectStore } from "@/hooks";

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
  getters: {
    /**
     * @return Layout options for the graph.
     */
    layoutOptions(): LayoutOptions {
      return {
        name: "preset",
        fit: false,
        positions: (node: NodeSingular | string) => {
          const id = typeof node === "string" ? node : node.data().id;

          return this.artifactPositions[id] || { x: 0, y: 0 };
        },
      };
    },
  },
  actions: {
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
        // Wait for the graph to render.
        cyResetTim();
        cyResetTree();
        appStore.onLoadEnd();
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
        // Wait for graph to render.
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
    /**
     * Updates artifact base positions.
     * If thee current document is the default, resets the layout.
     *
     * @param positions - The new positions to set.
     */
    async updateBasePositions(positions: ArtifactPositions): Promise<void> {
      projectStore.updateProject({ layout: positions });

      if (documentStore.currentId !== "") return;

      await this.updatePositions(positions);
    },
  },
});

export default useLayout(pinia);
