import { defineStore } from "pinia";

import {
  CollectionReturnValue,
  EventHandler,
  EventObject,
  NodeSingular,
} from "cytoscape";
import {
  CyPromise,
  CytoCore,
  CytoCoreGraph,
  CytoEvent,
  EdgeHandleCore,
  ResolveCy,
} from "@/types";
import { getTraceId } from "@/util";
import {
  appStore,
  selectionStore,
  traceApiStore,
  traceMatrixApiStore,
  traceStore,
} from "@/hooks";
import {
  GRAPH_CONFIG,
  CREATOR_PLUGINS,
  PROJECT_PLUGINS,
  DEFAULT_ARTIFACT_TREE_ZOOM,
  ZOOM_INCREMENT,
  CENTER_GRAPH_PADDING,
  ANIMATION_DURATION,
  EDGE_HANDLERS_OPTIONS,
} from "@/cytoscape";
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
      /**
       * Wraps creator cytoscape instance in a promise until it is created.
       */
      creatorResolveCy,
      /**
       * A promise for using the creator cy instance.
       */
      creatorCy,
      /**
       * Wraps project cytoscape instance in a promise until it is created.
       */
      projectResolveCy,
      /**
       * A promise for using the project cy instance.
       */
      projectCy,
      /**
       * The edge handles link drawing plugin.
       */
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
        config: GRAPH_CONFIG,
        saveCy: this.creatorResolveCy,
        plugins: CREATOR_PLUGINS,
        afterInit: () => this.centerNodes(false, "creator"),
      };
    },
    /**
     * @return The configuration for the project graph.
     */
    buildProjectGraph(): CytoCoreGraph {
      return {
        name: "artifact-tree-graph",
        config: GRAPH_CONFIG,
        saveCy: this.projectResolveCy,
        plugins: PROJECT_PLUGINS,
        afterInit: (cy) => {
          const selectedArtifacts = selectionStore.selectedArtifact?.id;

          if (!selectedArtifacts) {
            this.zoomReset();
            this.centerNodes();
          } else {
            selectionStore.centerOnArtifacts([selectedArtifacts]);
          }

          this.configureDrawMode(cy);
        },
      };
    },

    /**
     * Resets the graph window.
     * @param type - The type of graph to use.
     */
    resetWindow(type?: "project" | "creator" | "both") {
      if (type === "both" || type === "project") {
        const selectedId = selectionStore.selectedArtifact?.id;

        if (selectedId) {
          selectionStore.selectArtifact(selectedId);
        } else {
          this.centerNodes(false, "project");
        }
      }
      if (type === "both" || type === "creator") {
        this.creatorCy.then((cy) => {
          cy.fit(cy.nodes(), 150);
        });
      }
    },
    /**
     * Runs the given callback if cy is not animated.
     * @param callback - The callback to run.
     * @param type - The type of graph to use.
     */
    ifNotAnimated(callback: () => void, type?: "project" | "creator") {
      this.getCy(type).then((cy) => {
        if (!cy.animated()) {
          callback();
        }
      });
    },

    /**
     * Zooms the graph to the default zoom level.
     * @param type - The type of graph to use.
     */
    zoomReset(type?: "project" | "creator") {
      this.getCy(type).then((cy) => {
        cy.zoom(DEFAULT_ARTIFACT_TREE_ZOOM);
      });
    },
    /**
     * Zooms the graph in.
     * @param type - The type of graph to use.
     */
    zoomIn(type?: "project" | "creator") {
      this.getCy(type).then((cy) => {
        cy.zoom(cy.zoom() + ZOOM_INCREMENT);
      });
    },
    /**
     * Zooms the graph out.
     * @param type - The type of graph to use.
     */
    zoomOut(type?: "project" | "creator") {
      this.getCy(type).then((cy) => {
        cy.zoom(cy.zoom() - ZOOM_INCREMENT);
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

        if (animate) {
          if (cy.animated()) {
            cy.stop(false, false);
          }

          cy.animate({
            fit: { eles: nodes, padding: CENTER_GRAPH_PADDING },
            duration: ANIMATION_DURATION,
          });
        } else if (nodes.length > 10) {
          cy.fit(nodes, CENTER_GRAPH_PADDING);
        } else {
          cy.center(nodes);
        }
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

        cy.animate({
          zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
          center: { eles: collection },
          duration: ANIMATION_DURATION,
          complete: () => setCenteredArtifacts(undefined),
        });
      });
    },

    /**
     * Set the visibility of nodes and edges related to given list of artifact names.
     * @param artifactIds - The artifacts to display or hide.
     * @param visible - Whether to display or hide these artifacts.
     * @param type - The type of graph to use.
     */
    setDisplay(
      artifactIds: string[],
      visible: boolean,
      type?: "project" | "creator"
    ): void {
      const display = visible ? "element" : "none";

      this.getCy(type).then((cy) => {
        cy.nodes()
          .filter((n) => artifactIds.includes(n.data().id))
          .style({ display });

        cy.edges()
          .filter(
            (e) =>
              artifactIds.includes(e.target().data().id) &&
              artifactIds.includes(e.source().data().id)
          )
          .style({ display });
      });
    },
    /**
     * Shows all nodes and edges.
     * @param type - The type of graph to use.
     */
    displayAll(type?: "project" | "creator"): void {
      this.getCy(type).then((cy) => {
        cy.nodes().style({ display: "element" });
        cy.edges().style({ display: "element" });
      });
    },

    /**
     *  Enables draw mode for the graph.
     */
    drawMode(action: "enable" | "disable" | "toggle"): void {
      if (!this.edgeHandles) return;

      if (
        action === "disable" ||
        (action === "toggle" && appStore.popups.drawTrace)
      ) {
        this.edgeHandles.disableDrawMode();
        this.edgeHandles.disable();
        appStore.close("drawTrace");
      } else if (
        action === "enable" ||
        (action === "toggle" && !appStore.popups.drawTrace)
      ) {
        this.edgeHandles.enable();
        this.edgeHandles.enableDrawMode();
        appStore.open("drawTrace");
      }
    },
    /**
     * Initializes edge handles plugin for drawing links on the graph.
     * @param cy - The cytoscape instance.
     */
    configureDrawMode(cy: CytoCore): void {
      this.edgeHandles = cy.edgehandles({
        ...EDGE_HANDLERS_OPTIONS,
        canConnect: (source, target) =>
          traceStore.isLinkAllowed(source.data(), target.data()) === true,
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

        if (source.data()?.graph === "tree") {
          traceApiStore.handleCreate(source.data(), target.data());
        } else {
          traceMatrixApiStore.handleCreate(
            source.data().artifactType,
            target.data().artifactType
          );
        }
      }) as EventHandler);
    },
  },
});

export default useCy(pinia);
