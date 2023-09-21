import { defineStore } from "pinia";

import {
  EdgeSingular,
  EventObject,
  LayoutOptions,
  NodeSingular,
} from "cytoscape";
import {
  LayoutPositionsSchema,
  CyLayout,
  PositionSchema,
  GraphMode,
  CytoCore,
  AutoMoveReposition,
} from "@/types";
import { appStore, cyStore, selectionStore, subtreeStore } from "@/hooks";
import {
  ArtifactTreeAutoMoveHandlers,
  disableDrawMode,
  KlaySettings,
  GENERATED_LINK_SELECTOR,
  GENERATED_TRACE_MAX_WIDTH,
} from "@/cytoscape";
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
     * The current graph layout.
     */
    layout: undefined as CyLayout | undefined,
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
     * Creates a new graph layout.
     * @param type - The type of graph to reset.
     */
    createLayout(type?: "project" | "creator"): CyLayout {
      if (type === "creator") {
        return {
          klaySettings: KlaySettings,
          preLayoutHooks: [],
          postLayoutHooks: [this.applyCytoEvents],
          cytoEventHandlers: {},
          autoMoveHandlers: {},
        };
      } else {
        return {
          klaySettings: KlaySettings,
          preLayoutHooks: [this.styleGeneratedLinks],
          postLayoutHooks: [this.applyAutoMoveEvents, this.applyCytoEvents],
          cytoEventHandlers: {},
          autoMoveHandlers: ArtifactTreeAutoMoveHandlers,
        };
      }
    },
    /**
     * Resets the graph layout.
     * @param type - The type of graph to set the layout for.
     */
    setGraphLayout(type?: "project" | "creator"): void {
      const cyPromise = cyStore.getCy(type);
      const layout = this.createLayout(type);
      const generate =
        type === "creator"
          ? true
          : this.mode === "tim" ||
            Object.keys(this.artifactPositions).length === 0;

      appStore.onLoadStart();

      this.layout = layout;

      cyPromise.then((cy) => {
        layout.preLayoutHooks.forEach((hook) => hook(cy, layout));

        if (layout.klaySettings && generate) {
          cy.layout({
            name: "klay",
            klay: layout.klaySettings,
          }).run();
        } else {
          cy.layout(this.layoutOptions).run();
        }

        layout.postLayoutHooks.forEach((hook) => hook(cy, layout));

        this.applyAutomove();
      });

      // Wait for the graph to render.
      setTimeout(() => {
        cyStore.resetWindow("both");
        appStore.onLoadEnd();
      }, 200);
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
        this.setGraphLayout();
        appStore.onLoadEnd();
      }, 100);
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

      await this.resetLayout();
    },
    /**
     * Resets all automove events.
     */
    applyAutomove(): void {
      cyStore.getCy("project").then((cy) => {
        if (!this.layout) return;
        this.applyAutoMoveEvents(cy, this.layout);
      });
    },

    // Layout Hooks

    /**
     * Applies style changes to graph links.
     * @param cy - The cy instance.
     */
    styleGeneratedLinks(cy: CytoCore): void {
      cy.edges(GENERATED_LINK_SELECTOR).forEach((edge: EdgeSingular) => {
        const score = edge.data().score;

        edge.style({
          width: Math.min(
            score * GENERATED_TRACE_MAX_WIDTH,
            GENERATED_TRACE_MAX_WIDTH
          ),
        });
      });
    },
    /**
     * Applies cytoscape event handlers in the layout.
     * @param cy - The cy instance.
     * @param layout - The layout instance.
     */
    applyCytoEvents(cy: CytoCore, layout: CyLayout) {
      Object.values(layout.cytoEventHandlers).forEach((cytoEvent) => {
        const eventName = cytoEvent.events.join(" ");
        const selector = cytoEvent.selector;
        const handler = (event: EventObject) => cytoEvent.action(cy, event);

        if (selector === undefined) {
          cy.off(eventName);
          cy.on(eventName, handler);
        } else {
          cy.off(eventName, selector);
          cy.on(eventName, selector, handler);
        }
      });
    },
    /**
     * Adds auto-move handlers to all nodes, so that their children are dragged along with then.
     * @param cy - The cy instance.
     * @param layout - The layout instance.
     */
    applyAutoMoveEvents(cy: CytoCore, layout: CyLayout) {
      cy.automove("destroy");

      cy.nodes().forEach((node) => {
        const children = node
          .connectedEdges(`edge[source='${node.data().id}']`)
          .targets();

        const rule = cy.automove({
          nodesMatching: children.union(children.successors()),
          reposition: AutoMoveReposition.DRAG,
          dragWith: node,
        });

        for (const eventDefinition of Object.values(layout.autoMoveHandlers)) {
          node.on(eventDefinition.triggers.join(" "), (event: EventObject) => {
            eventDefinition.action(node, rule, event);
          });
        }
      });
    },
  },
});

export default useLayout(pinia);
