import { defineStore } from "pinia";

import {
  CollectionReturnValue,
  EventHandler,
  EventObject,
  NodeSingular,
} from "cytoscape";
import {
  CyConfiguration,
  CyPromise,
  CytoCore,
  CytoCoreGraph,
  CytoEvent,
  EdgeHandleCore,
  ResolveCy,
} from "@/types";
import { getTraceId, LARGE_NODE_COUNT } from "@/util";
import { appStore } from "@/hooks";
import { CYTO_CONFIG } from "@/cytoscape";
import { pinia } from "@/plugins";

/**
 * This hook manages the state of all cytoscape graphs.
 */
export const useCy = defineStore("cy", {
  state() {
    let creatorResolveCy: ResolveCy = null;
    let projectResolveCy: ResolveCy = null;
    const creatorCy: CyPromise = new Promise((resolve) => {
      creatorResolveCy = resolve;
    });
    const projectCy: CyPromise = new Promise((resolve) => {
      projectResolveCy = resolve;
    });

    return {
      /** Wraps creator cytoscape instance in a promise until it is created. */
      creatorResolveCy,
      /** A promise for using the creator cy instance. */
      creatorCy,
      /** Wraps project cytoscape instance in a promise until it is created. */
      projectResolveCy,
      /** A promise for using the project cy instance. */
      projectCy,
      /** The edge handles link drawing plugin. */
      edgeHandles: undefined as EdgeHandleCore | undefined,
    };
  },
  actions: {
    /**
     * Returns the cytoscape instance for the given type.
     * @param type - The type of graph to use.
     */
    getCy(type?: "project" | "creator"): CyPromise {
      return type === "creator" ? this.creatorCy : this.projectCy;
    },

    /**
     * @return The configuration for the creator graph.
     */
    buildCreatorGraph(): CytoCoreGraph {
      return {
        name: "tim-tree-graph",
        config: CYTO_CONFIG.GRAPH_CONFIG,
        saveCy: this.creatorResolveCy,
        plugins: CYTO_CONFIG.CREATOR_PLUGINS,
        afterInit: () => this.centerNodes(false, "creator"),
      };
    },
    /**
     * Builds a new cytoscape graph for the project.
     * @param config - The configuration for building a cytoscape graph.
     * @return The configuration for the project graph.
     */
    buildProjectGraph(config: CyConfiguration): CytoCoreGraph {
      return {
        name: "artifact-tree-graph",
        config: CYTO_CONFIG.GRAPH_CONFIG,
        saveCy: this.projectResolveCy,
        plugins: CYTO_CONFIG.PROJECT_PLUGINS,
        afterInit: (cy) => {
          this.resetWindow("project");
          this.configureDrawMode(cy, config);
        },
      };
    },
    /**
     * Resets the graph window.
     * @param type - The type of graph to use.
     */
    resetWindow(type?: "project" | "creator") {
      if (type !== "creator") {
        this.centerNodes(false, "project");
      } else {
        this.creatorCy.then((cy) => {
          cy.maxZoom(0.8);
          cy.fit(cy.nodes(), 150);
          cy.maxZoom(100);
        });
      }
    },
    /**
     * Zooms the graph in or out.
     * @param method - The zoom method to use.
     * @param type - The type of graph to use.
     */
    zoom(method: "in" | "out" | "reset", type?: "project" | "creator") {
      this.getCy(type).then((cy) => {
        if (method === "in") {
          cy.zoom(cy.zoom() + CYTO_CONFIG.ZOOM_INCREMENT);
        } else if (method === "out") {
          cy.zoom(cy.zoom() - CYTO_CONFIG.ZOOM_INCREMENT);
        } else {
          cy.zoom(CYTO_CONFIG.DEFAULT_ARTIFACT_TREE_ZOOM);
        }
      });
    },
    /**
     * Centers the viewport on all graph nodes.
     * @param animate - Whether to animate the centering.
     * @param type - The type of graph to use.
     */
    centerNodes(animate = false, type?: "project" | "creator"): void {
      this.getCy(type).then((cy) => {
        const nodes = cy.nodes();

        cy.maxZoom(0.8);

        if (animate) {
          if (cy.animated()) {
            cy.stop(false, false);
          }

          cy.animate({
            fit: { eles: nodes, padding: CYTO_CONFIG.CENTER_GRAPH_PADDING },
            duration: CYTO_CONFIG.ANIMATION_DURATION,
          });
        } else if (nodes.length > 10) {
          cy.fit(nodes, CYTO_CONFIG.CENTER_GRAPH_PADDING);
        } else {
          this.zoom("reset", type);
          cy.center(nodes);
        }

        cy.maxZoom(100);
      });
    },
    /**
     * Moves the viewport such that given set of artifacts is in the middle of the viewport.
     * If no artifacts are given, the entire collection of nodes is centered.
     * @param currentCenteringCollection - The current centered artifacts.
     * @param artifactIds - The artifacts whose average point will be centered.
     * @param setCenteredArtifacts - Sets the current centered artifacts.
     * @param type - The type of graph to use.
     */
    centerOnArtifacts(
      currentCenteringCollection: string[] | undefined,
      artifactIds: string[],
      setCenteredArtifacts: (ids: string[] | undefined) => void,
      type?: "project" | "creator"
    ): void {
      this.getCy(type).then((cy) => {
        if (cy.animated()) {
          cy.stop(false, false);
        }

        setCenteredArtifacts(artifactIds);

        const collection =
          artifactIds.length === 0
            ? cy.nodes()
            : cy.nodes().filter((n) => artifactIds.includes(n.data().id));

        cy.maxZoom(0.8);
        cy.animate({
          zoom: CYTO_CONFIG.DEFAULT_ARTIFACT_TREE_ZOOM,
          fit: { eles: collection, padding: CYTO_CONFIG.CENTER_GRAPH_PADDING },
          duration: CYTO_CONFIG.ANIMATION_DURATION,
          complete: () => setCenteredArtifacts(undefined),
        });
        cy.maxZoom(100);
      });
    },
    /**
     * Set the visibility of nodes and edges related to given list of artifact names.
     * if no artifact ids are given, all nodes and edges are set.
     * @param artifactIds - The artifacts to display or hide, or all if empty.
     * @param visible - Whether to display or hide these artifacts.
     * @param type - The type of graph to use.
     */
    setDisplay(
      artifactIds: string[],
      visible: boolean,
      type?: "project" | "creator"
    ): void {
      const display = visible ? "element" : "none";

      const doUpdateDisplay = (elDisplay: string | undefined, ids: string[]) =>
        // Update the display if changing to or from visible.
        elDisplay !== display &&
        (elDisplay === "none" || display === "none") &&
        // Update the display if the element is in the list of artifacts to update, or all are being updated.
        (artifactIds.length === 0 ||
          ids.every((id) => artifactIds.includes(id)));

      this.getCy(type).then((cy) => {
        cy.nodes()
          .filter((n) => doUpdateDisplay(n.style().display, [n.data().id]))
          .style({ display });

        cy.edges()
          .filter((e) =>
            doUpdateDisplay(e.style().display, [
              e.target().data().id,
              e.source().data().id,
            ])
          )
          .style({ display });
      });
    },
    /**
     *  Enables draw mode for the graph.
     */
    drawMode(action: "enable" | "disable" | "toggle"): void {
      if (
        action === "disable" ||
        (action === "toggle" && appStore.popups.drawTrace)
      ) {
        this.edgeHandles?.disableDrawMode();
        this.edgeHandles?.disable();
        appStore.close("drawTrace");
      } else if (
        action === "enable" ||
        (action === "toggle" && !appStore.popups.drawTrace)
      ) {
        this.edgeHandles?.enable();
        this.edgeHandles?.enableDrawMode();
        appStore.open("drawTrace");
      }
    },
    /**
     * Initializes edge handles plugin for drawing links on the graph.
     * @param cy - The cytoscape instance.
     * @param config - The configuration for building a cytoscape graph.
     */
    configureDrawMode(cy: CytoCore, config: CyConfiguration): void {
      this.edgeHandles = cy.edgehandles({
        ...CYTO_CONFIG.EDGE_HANDLERS_OPTIONS,
        canConnect: config.canCreateTrace,
        edgeParams: (source, target) => ({
          id: getTraceId(source.data().id, target.data().id),
          source: source.data().id,
          target: target.data().id,
        }),
      });

      cy.on(CytoEvent.EH_COMPLETE, ((
        event: EventObject,
        source: NodeSingular,
        target: NodeSingular,
        addedEdge: CollectionReturnValue
      ) => {
        this.drawMode("disable");
        addedEdge.remove();
        config.handleCreateTrace(source, target);
      }) as EventHandler);
    },
    /**
     * Run different operations based on the project size.
     * - Defaults to the large node count.
     * @param smaller - The operation to run if the project is smaller than the given size.
     * @param larger - The operation to run if the project is larger than the given size.
     * @param size - The size to compare against.
     */
    basedOnSize(
      smaller: (cy: CytoCore) => void,
      larger?: (cy: CytoCore) => void,
      size = LARGE_NODE_COUNT
    ) {
      this.getCy("project").then((cy) => {
        if (cy.nodes().length > size) {
          larger?.(cy);
        } else {
          smaller(cy);
        }
      });
    },
  },
});

export default useCy(pinia);
