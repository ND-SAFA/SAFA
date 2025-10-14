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
import { LARGE_NODE_LAYOUT_COUNT, GENERATION_SCORE_VALUES } from "@/util";
import { appStore, cyStore } from "@/hooks";
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
     * @return Whether the graph is in TIM mode.
     */
    isTimMode(): boolean {
      return this.mode === "tim";
    },
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
     * @return Whether the graph is in chat mode.
     */
    isChatMode(): boolean {
      return this.mode === "chat";
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
      const generate =
        animated ||
        type === "creator" ||
        this.mode === "tim" ||
        Object.keys(this.artifactPositions).length === 0;

      cyStore.getCy(type).then((cy) => {
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

        cyStore.drawMode("disable");
        this.styleGeneratedLinks();
        this.applyAutomove();

        if (
          this.mode === "tim" &&
          type !== "creator" &&
          appStore.popups.detailsPanel !== "displayProject" &&
          cy.nodes().length > 0
        ) {
          // On the TIM page, open the project details panel, then recenter the layout after it opens.
          appStore.openDetailsPanel("displayProject");
          setTimeout(() => cyStore.centerNodes(true), 400);
        }

        // Wait for the graph to render and panel to open, then center on the nodes.
        setTimeout(() => {
          if (animated) return;

          if (this.mode === "tim" && type !== "creator") {
            cyStore.centerNodes(true);
          } else {
            cyStore.resetWindow(type);
          }

          appStore.onLoadEnd();
        }, 350);
      });
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
     * @param visibleArtifacts - The number of visible artifacts.
     */
    async updatePositions(
      positions: LayoutPositionsSchema,
      visibleArtifacts: number
    ): Promise<void> {
      this.artifactPositions = positions;

      if (
        visibleArtifacts === 0 ||
        visibleArtifacts > LARGE_NODE_LAYOUT_COUNT
      ) {
        this.setGraphLayout("project", false);
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
      cyStore.basedOnSize((cy) => {
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
     * Sets the width of generated links to reflect their score.
     * - This action is skipped if the graph is too large.
     */
    styleGeneratedLinks(): void {
      cyStore.basedOnSize((cy) => {
        cy.edges(CYTO_CONFIG.GENERATED_LINK_SELECTOR).forEach((edge) => {
          const width =
            (edge.data().score >= GENERATION_SCORE_VALUES.HIGH
              ? CYTO_CONFIG.GENERATED_TRACE_MAX_WIDTH
              : edge.data().score >= GENERATION_SCORE_VALUES.MEDIUM
                ? CYTO_CONFIG.GENERATED_TRACE_MAX_WIDTH / 2
                : CYTO_CONFIG.GENERATED_TRACE_MAX_WIDTH / 3) *
            edge.data().score;

          edge.style({ width });
        });
      });
    },
  },
});

export default useLayout(pinia);
