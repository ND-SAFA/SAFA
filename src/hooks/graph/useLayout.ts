import { defineStore } from "pinia";

import { EventObject, LayoutOptions, NodeSingular } from "cytoscape";
import {
  LayoutPositionsSchema,
  PositionSchema,
  GraphMode,
  AutoMoveReposition,
  CytoEvent,
  CSSCursor,
} from "@/types";
import { LARGE_NODE_LAYOUT_COUNT } from "@/util";
import {
  appStore,
  artifactStore,
  cyStore,
  selectionStore,
  subtreeStore,
} from "@/hooks";
import { CYTO_CONFIG } from "@/cytoscape";
import { pinia } from "@/plugins";

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
     * The current view mode of the graph.
     */
    mode: "tim" as GraphMode,
  }),
  getters: {
    /**
     * @return Whether the graph is in tree mode.
     */
    isTreeMode(): boolean {
      return this.mode === "tree";
    },
    /**
     * @return Whether the graph is in table mode.
     */
    isTableMode(): boolean {
      return this.mode === "table";
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
     * Resets the graph layout.
     * @param type - The type of graph to set the layout for.
     * @param animated - Whether to animate the layout, and keep the graph displayed.
     */
    setGraphLayout(type?: "project" | "creator", animated?: boolean): void {
      const cyPromise = cyStore.getCy(type);
      const generate =
        animated ||
        type === "creator" ||
        this.mode === "tim" ||
        Object.keys(this.artifactPositions).length === 0;

      cyPromise.then((cy) => {
        if (!animated) appStore.onLoadStart();

        if (generate) {
          cy.layout({
            name: "klay",
            klay: CYTO_CONFIG.KLAY_CONFIG,
            animate: animated,
            animationDuration: CYTO_CONFIG.ANIMATION_DURATION,
            padding: CYTO_CONFIG.CENTER_GRAPH_PADDING,
          }).run();
        } else {
          cy.layout(this.layoutOptions).run();
        }

        this.styleGeneratedLinks();
        this.applyAutomove();

        if (!animated) {
          // Wait for the graph to render.
          setTimeout(() => {
            cyStore.resetWindow(type);
            appStore.onLoadEnd();
          }, 300);
        }

        if (this.mode === "tim") {
          appStore.openDetailsPanel("displayProject");
        }
      });
    },
    /**
     * Resets the layout of the graph.
     */
    async resetLayout(): Promise<void> {
      appStore.onLoadStart();

      cyStore.drawMode("disable");
      subtreeStore.resetHiddenNodes();
      selectionStore.clearSelections();
      appStore.closeSidePanels();
      this.setGraphLayout();

      appStore.onLoadEnd();
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
     * Updates artifact positions and resets the layout.
     *
     * @param positions - The new positions to set.
     */
    async updatePositions(positions: LayoutPositionsSchema): Promise<void> {
      this.artifactPositions = positions;

      if (artifactStore.currentArtifacts.length > LARGE_NODE_LAYOUT_COUNT) {
        await this.resetLayout();
      } else {
        this.setGraphLayout("project", true);
        cyStore.centerNodes(true);
      }
    },
    /**
     * Adds auto-move handlers to all nodes, so that their children are dragged along with then.
     * - This action is skipped if the graph is too large.
     */
    applyAutomove(): void {
      if (artifactStore.largeNodeCount) return;

      cyStore.getCy("project").then((cy) => {
        cy.automove("destroy");

        cy.nodes().forEach((node) => {
          const children = node
            .connectedEdges(`edge[source='${node.data().id}']`)
            .targets();

          cy.automove({
            nodesMatching: children.union(children.successors()),
            reposition: AutoMoveReposition.DRAG,
            dragWith: node,
          });

          node.on(CytoEvent.CXT_TAP, (event: EventObject) => {
            document.body.style.cursor = CSSCursor.GRAB;
            const nodePosition = event.target.renderedPosition();
            event.target.renderedPosition({
              x: nodePosition.x + event.originalEvent.movementX / 2,
              y: nodePosition.y + event.originalEvent.movementY / 2,
            });
          });
        });
      });
    },
    /**
     * Applies style changes to graph links.
     * - This action is skipped if the graph is too large.
     */
    styleGeneratedLinks(): void {
      if (artifactStore.largeNodeCount) return;

      cyStore.getCy("project").then((cy) => {
        cy.edges(CYTO_CONFIG.GENERATED_LINK_SELECTOR).forEach((edge) => {
          edge.style({
            width: Math.min(
              edge.data().score * CYTO_CONFIG.GENERATED_TRACE_MAX_WIDTH,
              CYTO_CONFIG.GENERATED_TRACE_MAX_WIDTH
            ),
          });
        });
      });
    },
  },
});

export default useLayout(pinia);
