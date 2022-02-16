import { CyPromise, LayoutPayload } from "@/types";
import { artifactTreeCyPromise } from "@/cytoscape/cy";
import {
  ANIMATION_DURATION,
  CENTER_GRAPH_PADDING,
  DEFAULT_ARTIFACT_TREE_ZOOM,
  ZOOM_INCREMENT,
} from "@/cytoscape/styles";
import { appModule, logModule, viewportModule } from "@/store";
import { areArraysEqual } from "@/util";

/**
 * Runs the given callback if cy is not animated.
 *
 * @param cb - The callback to run.
 * @param cyPromise - The cy instance.
 */
export function cyIfNotAnimated(
  cb: () => void,
  cyPromise: CyPromise = artifactTreeCyPromise
): void {
  cyPromise.then((cy) => {
    if (!cy.animated()) {
      cb();
    }
  });
}

/**
 * Resets the zoom level.
 *
 * @param cyPromise - The cy instance.
 */
export function cyZoomReset(
  cyPromise: CyPromise = artifactTreeCyPromise
): void {
  cyPromise.then((cy) => {
    cy.zoom(DEFAULT_ARTIFACT_TREE_ZOOM);
  });
}

/**
 * Zooms in the viewport.
 *
 * @param cyPromise - The cy instance.
 */
export function cyZoomIn(cyPromise: CyPromise = artifactTreeCyPromise): void {
  cyPromise.then((cy) => {
    cy.zoom(cy.zoom() + ZOOM_INCREMENT);
    cy.center(cy.nodes());
  });
}

/**
 * Zooms out the viewport.
 *
 * @param cyPromise - The cy instance.
 */
export function cyZoomOut(cyPromise: CyPromise = artifactTreeCyPromise): void {
  cyPromise.then((cy) => {
    cy.zoom(cy.zoom() - ZOOM_INCREMENT);
    cy.center(cy.nodes());
  });
}

/**
 * Centers the viewport on all graph nodes.
 *
 * @param cyPromise - The cy instance.
 */
export function cyCenterNodes(
  cyPromise: CyPromise = artifactTreeCyPromise
): void {
  cyPromise.then((cy) => {
    cy.center(cy.nodes());
  });
}

/**
 * Creates the given layout.
 *
 * @param layoutPayload - The cy instance and layout.
 */
export function cyCreateLayout(layoutPayload: LayoutPayload): void {
  layoutPayload.cyPromise.then((cy) => {
    layoutPayload.layout.createLayout(cy);
  });
}

/**
 * Moves the viewport such that given set of artifacts is in the middle of the viewport.
 * If no artifacts are given, the entire collection of nodes is centered.
 * Request is ignored if current animation is in progress to center the same collection of artifacts.
 *
 * @param currentCenteringCollection - The current centered artifacts.
 * @param artifactIds - The artifacts whose average point will be centered.
 * @param setCenteredArtifacts - Sets the current centered artifacts.
 * @param cyPromise - A promise returning an instance of cytoscape.
 */
export function cyCenterOnArtifacts(
  currentCenteringCollection: string[] | undefined,
  artifactIds: string[],
  setCenteredArtifacts: (ids: string[] | undefined) => void,
  cyPromise = artifactTreeCyPromise
): void {
  cyPromise.then((cy) => {
    if (cy.animated()) {
      if (
        currentCenteringCollection !== undefined &&
        areArraysEqual(currentCenteringCollection, artifactIds)
      ) {
        return logModule.onDevWarning(
          `Collection is already being rendered: ${artifactIds}`
        );
      } else {
        cy.stop(false, false);
      }
    }

    setCenteredArtifacts(artifactIds);

    const collection =
      artifactIds.length === 0
        ? cy.nodes()
        : cy.nodes().filter((n) => artifactIds.includes(n.data().id));

    if (collection.length > 1) {
      cy.animate({
        fit: { eles: collection, padding: CENTER_GRAPH_PADDING },
        duration: ANIMATION_DURATION,
        complete: () => setCenteredArtifacts(undefined),
      });
    } else {
      cy.animate({
        zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
        center: { eles: collection },
        duration: ANIMATION_DURATION,
        complete: () => setCenteredArtifacts(undefined),
      });
    }
  });
}

/**
 * Set the visibility of nodes and edges related to given list of artifact names.
 * A node is related if it represents one of the target artifacts.
 * An edge is related if either source or target is an artifact in target
 * list.
 *
 * @param artifactIds - The artifacts to display or hide.
 * @param visible - Whether to display or hide these artifacts.
 * @param cyPromise - The cy instance.
 */
export function cySetDisplay(
  artifactIds: string[],
  visible: boolean,
  cyPromise: CyPromise = artifactTreeCyPromise
): void {
  const display = visible ? "element" : "none";

  cyPromise.then((cy) => {
    cy.nodes()
      .filter((n) => artifactIds.includes(n.data().id))
      .style({ display });

    cy.edges()
      .filter(
        (e) =>
          artifactIds.includes(e.target().data().id) ||
          artifactIds.includes(e.source().data().id)
      )
      .style({ display });
  });
}

/**
 * Shows all nodes and edges.
 *
 * @param cyPromise - The cy instance.
 */
export function cyDisplayAll(
  cyPromise: CyPromise = artifactTreeCyPromise
): void {
  cyPromise.then((cy) => {
    cy.nodes().style({ display: "element" });
    cy.edges().style({ display: "element" });
  });
}
