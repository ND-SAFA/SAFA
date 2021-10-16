import { NodeSingular, NodeCollection } from "cytoscape";

/**
 * Types were manually constructed from https://github.com/cytoscape/cytoscape.js-automove
 */

type NodeSelectionFunction = (node: NodeSingular) => boolean;

export enum AutoMoveReposition {
  MEAN = "mean",
  VIEWPORT = "viewport",
  DRAG = "drag",
}

enum AutoMoveBoundingBoxType {
  INSIDE = "inside",
  OUTSIDE = "outside",
}
interface AutoMoveBoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  type?: AutoMoveBoundingBoxType;
}

interface NodePosition {
  x: number;
  y: number;
}

type NodePositioningFunction = (node: NodeSingular) => NodePosition;
type UpdateCallback = () => void;
type UpdateHandler = (update: UpdateCallback) => void;

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

export interface AutoMoveRule {
  apply: () => void; // manually apply a rule
  enabled: () => boolean; // get whether rule is enabled
  toggle: () => void; // toggle whether the rule is enabled
  disable: () => void; // temporarily disable the rule
  enable: () => void; // re-enable the rule
  destroy: () => void; // remove and clean up just this rule
}
