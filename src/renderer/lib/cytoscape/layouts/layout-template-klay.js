import LayoutBaseTemplate from '.'

export default class LayoutTemplateKlay extends LayoutBaseTemplate {
  static NODE_PLACEMENT = {
    BRANDES_KOEPF: 'BRANDES_KOEPF', // Minimizes the number of edge bends at the expense of diagram size: diagrams drawn with this algorithm are usually higher than diagrams drawn with other algorithms.
    LINEAR_SEGMENTS: 'LINEAR_SEGMENTS', // Computes a balanced placement.
    INTERACTIVE: 'INTERACTIVE', // Tries to keep the preset y coordinates of nodes from the original layout. For dummy nodes, a guess is made to infer their coordinates. Requires the other interactive phase implementations to have run as well.
    SIMPLE: 'SIMPLE' // Minimizes the area at the expense of... well, pretty much everything else.
  }

  static NODE_LAYERING = {
    NETWORK_SIMPLEX: 'NETWORK_SIMPLEX', // This algorithm tries to minimize the length of edges. This is the most computationally intensive algorithm. The number of iterations after which it aborts if it hasn't found a result yet can be set with the Maximal Iterations option.
    LONGEST_PATH: 'LONGEST_PATH', // A very simple algorithm that distributes nodes along their longest path to a sink node.
    INTERACTIVE: 'INTERACTIVE' // Distributes the nodes into layers by comparing their positions before the layout algorithm was started. The idea is that the relative horizontal order of nodes as it was before layout was applied is not changed. This of course requires valid positions for all nodes to have been set on the input graph before calling the layout algorithm. The interactive node layering algorithm uses the Interactive Reference Point option to determine which reference point of nodes are used to compare positions.
  }

  static FIXED_ALIGNMENT = {
    NONE: 'NONE', // Chooses the smallest layout from the four possible candidates.
    LEFTUP: 'LEFTUP', // Chooses the left-up candidate from the four possible candidates.
    RIGHTUP: 'RIGHTUP', // Chooses the right-up candidate from the four possible candidates.
    LEFTDOWN: 'LEFTDOWN', // Chooses the left-down candidate from the four possible candidates.
    RIGHTDOWN: 'RIGHTDOWN', // Chooses the right-down candidate from the four possible candidates.
    BALANCED: 'BALANCED' // Creates a balanced layout from the four possible candidates. */
  }

  static DIRECTION = {
    // Overall direction of edges: horizontal (right / left) or vertical (down / up)
    UNDEFINED: 'UNDEFINED',
    RIGHT: 'RIGHT',
    LEFT: 'LEFT',
    DOWN: 'DOWN',
    UP: 'UP'
  }

  constructor (options) {
    super(options.zoom || 1, options.pan || { x: 0, y: 0 })
    this.__name = 'klay'
    this.klay = {}
    this.klay.spacing = options.spacing || 15 // Overall setting for the minimal amount of space to be left between objects
    this.klay.direction = options.direction || LayoutTemplateKlay.DIRECTION.UP
    this.klay.fixedAlignment = options.fixedAlignment || LayoutTemplateKlay.FIXED_ALIGNMENT.BALANCED
    this.klay.layoutHierarchy = options.layoutHierarchy || true
    this.klay.nodeLayering = options.nodeLayering || LayoutTemplateKlay.NODE_LAYERING.NETWORK_SIMPLEX
    this.klay.nodePlacement = options.nodePlacement || LayoutTemplateKlay.NODE_PLACEMENT.LINEAR_SEGMENTS
    this.klay.inLayerSpacingFactor = options.inLayerSpacingFactor || 0.4
    this.klay.thoroughness = options.thoroughness || 10
  }

  makeLayout (cy) {
    const { name, zoom, pan, klay } = this
    return cy.layout({name, zoom, pan, klay})
  }
}
