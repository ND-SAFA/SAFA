import { defineStore } from "pinia";

import { LayoutOptions, NodeSingular } from "cytoscape";
import {
  LayoutPositionsSchema,
  CyLayout,
  LayoutPayload,
  PositionSchema,
  GraphMode,
} from "@/types";
import { typeOptionsStore } from "@/hooks";
import {
  artifactTreeCyPromise,
  cyApplyAutomove,
  cyCreateLayout,
  cyResetTim,
  cyResetTree,
  disableDrawMode,
  timTreeCyPromise,
  GraphLayout,
} from "@/cytoscape";
import { pinia } from "@/plugins";
import { appStore } from "@/hooks/core";
import selectionStore from "@/hooks/graph/useSelection";
import subtreeStore from "@/hooks/project/useSubtree";

/**
 * This module handles the layout positions of the graph.
 */
export const useLayout = defineStore("layout", {
  state: () => ({
    /**
     * A mapping from artifact ID to its position.
     */
    artifactPositions: {} as LayoutPositionsSchema,
    /**
     * A saved position for a node to be added.
     */
    savedPosition: undefined as PositionSchema | undefined,
    /**
     * The current graph layout.
     */
    layout: undefined as CyLayout | undefined,
    /**
     * The current view mode of the graph.
     */
    mode: GraphMode.tim as GraphMode,
  }),
  getters: {
    /**
     * @return Whether the graph is in tree mode.
     */
    isTreeMode(): boolean {
      return this.mode === GraphMode.tree;
    },
    /**
     * @return Whether the graph is in table mode.
     */
    isTableMode(): boolean {
      return this.mode === GraphMode.table;
    },
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
     *
     * @param layoutPayload - The cy instance and layout.
     * @param generate - Whether to generate the layout positions.
     */
    setGraphLayout(layoutPayload: LayoutPayload, generate?: boolean): void {
      appStore.onLoadStart();

      this.layout = layoutPayload.layout;
      cyCreateLayout(layoutPayload, generate);
      this.applyAutomove();

      // Wait for the graph to render.
      setTimeout(() => {
        cyResetTim();
        cyResetTree();
        appStore.onLoadEnd();
      }, 200);
    },
    /**
     * Resets the graph layout of the artifact tree.
     * Generates a new layout if in TIM view, or if no positions are set.
     */
    setArtifactTreeLayout(): void {
      const layout = GraphLayout.createArtifactLayout();
      const payload = { layout, cyPromise: artifactTreeCyPromise };
      const generateLayout =
        this.mode === GraphMode.tim ||
        Object.keys(this.artifactPositions).length === 0;

      this.setGraphLayout(payload, generateLayout);
    },
    /**
     * Resets the graph layout of the TIM tree.
     */
    setTimTreeLayout(): void {
      const layout = GraphLayout.createTimLayout();
      const payload = { layout, cyPromise: timTreeCyPromise };

      this.setGraphLayout(payload, true);
    },
    /**
     * Resets the layout of the graph.
     */
    async resetLayout(): Promise<void> {
      appStore.onLoadStart();

      disableDrawMode();
      subtreeStore.resetHiddenNodes();
      selectionStore.clearSelections();
      appStore.closeSidePanels();

      // Wait for graph to render.
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
    async updatePositions(positions: LayoutPositionsSchema): Promise<void> {
      this.artifactPositions = positions;

      await this.resetLayout();
    },
    /**
     * Switches the layout to tree mode, and only displays the listed types.
     *
     * @param visibleTypes - The types to display.
     */
    viewTreeTypes(visibleTypes: string[]): void {
      const hiddenTypes = typeOptionsStore.artifactTypes.filter(
        (type) => !visibleTypes.includes(type)
      );

      this.mode = GraphMode.tree;

      hiddenTypes.forEach((ignoreType) => {
        selectionStore.filterGraph({
          type: "ignore",
          action: "add",
          ignoreType,
        });
      });
    },
  },
});

export default useLayout(pinia);
