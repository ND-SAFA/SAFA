import * as GraphOptions from '@/components/Main/FaultTree/GraphOptions'

const G = GraphOptions

export default [
  {
    selector: 'edge',
    style: {
      'curve-style': G.EDGE_CURVE_STYLE
    }
  },
  {
    selector: 'node',
    style: {
      'background-color': G.NODE_COLOR,
      padding: G.NODE_PADDING,
      shape: G.NODE_SHAPE,
      width: G.NODE_WIDTH,
      height: G.NODE_HEIGHT,
      'border-style': G.NODE_BORDER_STYLE,
      'border-width': G.NODE_BORDER_WIDTH
    }
  },
  {
    selector: 'node.logical-gate',
    style: {
      'border-width': G.LOGICAL_GATE_BORDER_WIDTH,
      padding: G.LOGICAL_GATE_PADDING,
      width: G.LOGICAL_GATE_WIDTH,
      height: G.LOGICAL_GATE_HEIGHT
    }
  },
  {
    selector: 'node:selected',
    style: {
      'background-color': G.NODE_SELECTED_COLOR
    }
  }
]
