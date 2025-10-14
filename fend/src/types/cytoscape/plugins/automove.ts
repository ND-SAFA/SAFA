import { NodeSingular, NodeCollection } from "cytoscape";
import { EmptyLambda } from "@/types";

/**
 * Types were manually constructed from: https://github.com/cytoscape/cytoscape.js-automove
 */

/**
 * Returns whether to select the given node.
 */
type NodeSelectionFunction = (node: NodeSingular) => boolean;

/**
 * Enumerates the types of auto move repositions.
 */
export enum AutoMoveReposition {
  MEAN = "mean",
  VIEWPORT = "viewport",
  DRAG = "drag",
}

/**
 * Enumerates the types of bounding boxes.
 */
enum AutoMoveBoundingBoxType {
  INSIDE = "inside",
  OUTSIDE = "outside",
}

/**
 * Defines a bounding box.
 */
interface AutoMoveBoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  type?: AutoMoveBoundingBoxType;
}

/**
 * Defines the position of a node.
 */
interface NodePosition {
  x: number;
  y: number;
}

/**
 * Returns an updated position of the given node.
 */
type NodePositioningFunction = (node: NodeSingular) => NodePosition;

/**
 * Run when an update is made.
 */
type UpdateHandler = (update: EmptyLambda) => void;

/**
 * Defines the options for auto moving a node.
 */
export interface AutoMoveOptions {
  nodesMatching?: NodeSelectionFunction | string | NodeCollection;
  reposition?:
    | AutoMoveReposition
    | AutoMoveBoundingBox
    | NodePositioningFunction;
  when?: UpdateHandler | "matching";
  meanIgnores?: NodeSelectionFunction;
  meanOnSelfPosition?: NodeSelectionFunction;
  dragWith?: NodeSelectionFunction | string | NodeCollection | NodeSingular;
}

/**
 * Defines rule callbacks for an auto move.
 */
export interface AutoMoveRule {
  /**
   * Manually applies a rule.
   */
  apply(): void;
  /**
   * Returns whether a rule is enabled.
   */
  enabled(): boolean;
  /**
   * Toggles whether the rule is enabled.
   */
  toggle(): void;
  /**
   * Temporarily disables the rule.
   */
  disable(): void;
  /**
   * Re-enables a disabled rule.
   */
  enable(): void;
  /**
   * Removes and cleans up this rule.
   */
  destroy(): void;
}
