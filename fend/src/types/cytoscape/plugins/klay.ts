/**
 * Types were extracted from: https://github.com/cytoscape/cytoscape.js-klay
 */

/**
 * Enumerates the overall direction of edges: horizontal (right / left) or vertical (down / up).
 */
export enum LayoutDirection {
  UNDEFINED = "UNDEFINED",
  RIGHT = "RIGHT",
  LEFT = "LEFT",
  DOWN = "DOWN",
  UP = "UP",
}

/**
 * Enumerates the alignment to tell the BK node placer to use a certain alignment instead of taking the optimal result.
 */
export enum FixedAlignment {
  /**
   * Chooses the smallest layout from the four possible candidates.
   */
  NONE = "NONE",
  /**
   * Chooses the left-up candidate from the four possible candidates.
   */
  LEFTUP = "LEFTUP",
  /**
   * Chooses the right-up candidate from the four possible candidates.
   */
  RIGHTUP = "RIGHTUP",
  /**
   * Chooses the left-down candidate from the four possible candidates.
   */
  LEFTDOWN = "LEFTDOWN",
  /**
   * Chooses the right-down candidate from the four possible candidates.
   */
  RIGHTDOWN = "RIGHTDOWN",
  /**
   * Creates a balanced layout from the four possible candidates.
   */
  BALANCED = "BALANCED",
}

/**
 * Enumerates the strategies for node layering.
 */
export enum NodeLayering {
  /**
   * This algorithm tries to minimize the length of edges. This is the most computationally intensive algorithm.
   * The number of iterations after which it aborts if it hasn't found a result yet can be set with the Maximal
   * Iterations option.
   */
  NETWORK_SIMPLEX = "NETWORK_SIMPLEX",
  /**
   * A very simple algorithm that distributes nodes along their longest path to a sink node.
   */
  LONGEST_PATH = "LONGEST_PATH",
  /**
   * Distributes the nodes into layers by comparing their positions before the layout algorithm was started.
   * The idea is that the relative horizontal order of nodes as it was before layout was applied is not changed.
   * This of course requires valid positions for all nodes to have been set on the input graph before calling the
   * layout algorithm. The interactive node layering algorithm uses the Interactive Reference Point option to
   * determine which reference point of nodes are used to compare positions.
   */
  INTERACTIVE = "INTERACTIVE",
}

/**
 * Enumerates types of node placement.
 */
export enum NodePlacement {
  /**
   * Minimizes the number of edge bends at the expense of diagram size: diagrams drawn with this algorithm are
   * usually higher than diagrams drawn with other algorithms.
   */
  BRANDES_KOEPF = "BRANDES_KOEPF",
  /**
   * Computes a balanced placement.
   */
  LINEAR_SEGMENTS = "LINEAR_SEGMENTS",
  /**
   * Tries to keep the preset y coordinates of nodes from the original layout. For dummy nodes, a guess is made to infer their coordinates. Requires the other interactive phase implementations to have run as well.
   */
  INTERACTIVE = "INTERACTIVE",
  /**
   * Minimizes the area at the expense of... well, pretty much everything else.
   */
  SIMPLE = "SIMPLE",
}

/**
 * Enumerates types of node shapes.
 */
export enum NodePlacement {
  ROUND_RECTANGLE = "round-rectangle",
  RECTANGLE = "rectangle",
  ELLIPSE = "ellipse",
  POLYGON = "polygon",
}

/**
 * Defines the klay layout settings.
 */
export interface KlayLayoutSettings {
  spacing?: number;
  direction?: LayoutDirection;
  fixedAlignment?: FixedAlignment;
  layoutHierarchy?: boolean;
  nodeLayering?: NodeLayering;
  nodePlacement?: NodePlacement;
  inLayerSpacingFactor?: number;
  thoroughness?: number;
  randomizationSeed?: number;
}

/**
 * Defines the klay layout options.
 * https://github.com/cytoscape/cytoscape.js-klay/blob/master/src/defaults.js
 */
export interface KlayLayoutOptions {
  name: "klay";
  klay: KlayLayoutSettings;
  animate?: boolean;
  animationDuration?: number;
  fit?: boolean;
  padding?: number;
}
