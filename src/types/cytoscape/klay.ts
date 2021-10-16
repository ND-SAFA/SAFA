import IGraphLayout from "@/types/cytoscape/igraph-layout";
import { CytoCore } from "@/types/cytoscape";

/**
 * Types were extracted from: https://github.com/cytoscape/cytoscape.js-klay
 */
export enum LayoutDirection { // Overall direction of edges: horizontal (right / left) or vertical (down / up)
  UNDEFINED = "UNDEFINED",
  RIGHT = "RIGHT",
  LEFT = "LEFT",
  DOWN = "DOWN",
  UP = "UP",
}

export enum FixedAlignment { // Tells the BK node placer to use a certain alignment instead of taking the optimal result.
  NONE = "NONE", // Chooses the smallest layout from the four possible candidates.
  LEFTUP = "LEFTUP", // Chooses the left-up candidate from the four possible candidates.
  RIGHTUP = "RIGHTUP", // Chooses the right-up candidate from the four possible candidates.
  LEFTDOWN = "LEFTDOWN", // Chooses the left-down candidate from the four possible candidates.
  RIGHTDOWN = "RIGHTDOWN", // Chooses the right-down candidate from the four possible candidates.
  BALANCED = "BALANCED", // Creates a balanced layout from the four possible candidates. */
}

export enum NodeLayering { // Strategy for node layering.
  NETWORK_SIMPLEX = "NETWORK_SIMPLEX", // This algorithm tries to minimize the length of edges. This is the most computationally intensive algorithm. The number of iterations after which it aborts if it hasn't found a result yet can be set with the Maximal Iterations option.
  LONGEST_PATH = "LONGEST_PATH", // A very simple algorithm that distributes nodes along their longest path to a sink node.
  INTERACTIVE = "INTERACTIVE", // Distributes the nodes into layers by comparing their positions before the layout algorithm was started. The idea is that the relative horizontal order of nodes as it was before layout was applied is not changed. This of course requires valid positions for all nodes to have been set on the input graph before calling the layout algorithm. The interactive node layering algorithm uses the Interactive Reference Point option to determine which reference point of nodes are used to compare positions.
}

export enum NodePlacement {
  BRANDES_KOEPF = "BRANDES_KOEPF", // Minimizes the number of edge bends at the expense of diagram size: diagrams drawn with this algorithm are usually higher than diagrams drawn with other algorithms.
  LINEAR_SEGMENTS = "LINEAR_SEGMENTS", // Computes a balanced placement.
  INTERACTIVE = "INTERACTIVE", // Tries to keep the preset y coordinates of nodes from the original layout. For dummy nodes, a guess is made to infer their coordinates. Requires the other interactive phase implementations to have run as well.
  SIMPLE = "SIMPLE", // Minimizes the area at the expense of... well, pretty much everything else.
}

export interface KlayLayoutSettings {
  spacing: number;
  direction: LayoutDirection;
  fixedAlignment: FixedAlignment;
  layoutHierarchy: boolean;
  nodeLayering: NodeLayering;
  nodePlacement: NodePlacement;
  inLayerSpacingFactor: number;
  thoroughness: number;
  randomizationSeed: number;
}

export interface KlayLayoutOptions {
  name: "klay";
  klay: KlayLayoutSettings;
}
export type LayoutHook = (cy: CytoCore, layout: IGraphLayout) => void;
