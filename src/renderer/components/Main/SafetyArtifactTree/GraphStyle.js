import * as GraphOptions from '@/components/Main/SafetyArtifactTree/GraphOptions'

export default [
  {
    selector: 'edge',
    style: {
      'curve-style': GraphOptions.EDGE_CURVE_STYLE,
      'width': '1px',
      'line-color': '#000000'
    }
  },
  {
    selector: 'node',
    style: {
      'background-color': GraphOptions.NODE_COLOR,
      padding: GraphOptions.NODE_PADDING,
      shape: GraphOptions.NODE_SHAPE,
      width: GraphOptions.NODE_WIDTH,
      height: GraphOptions.NODE_HEIGHT,
      'border-style': GraphOptions.NODE_BORDER_STYLE,
      'border-width': GraphOptions.NODE_BORDER_WIDTH,
      'overlay-opacity': GraphOptions.NODE_OVERLAY_OPACITY
    }
  },
  {
    selector: '.added',
    style: {
      // node styling
      'background-color': GraphOptions.DELTA_NODE_ADDED_COLOR,
      'border-color': GraphOptions.DELTA_NODE_ADDED_BORDER_COLOR,
      // edge styling
      'line-color': GraphOptions.DELTA_EDGE_ADDED_LINE_COLOR
    }
  },
  {
    selector: '.modified',
    style: {
      // node styling
      'background-color': GraphOptions.DELTA_NODE_MODIFIED_COLOR,
      'border-color': GraphOptions.DELTA_NODE_MODIFIED_BORDER_COLOR,
      // edge styling
      'line-color': GraphOptions.DELTA_EDGE_MODIFIED_LINE_COLOR
    }
  },
  {
    selector: '.removed',
    style: {
      // node styling
      shape: GraphOptions.DELTA_NODE_REMOVED_SHAPE,
      'background-color': GraphOptions.DELTA_NODE_REMOVED_COLOR,
      'border-color': GraphOptions.DELTA_NODE_REMOVED_BORDER_COLOR,
      // edge styling
      'line-color': GraphOptions.DELTA_EDGE_REMOVED_LINE_COLOR
    }
  },
  {
    selector: '.warning',
    style: {
      height: GraphOptions.NODE_WARNING_HEIGHT
    }
  },
  {
    selector: '.code-node',
    style: {
      height: GraphOptions.NODE_CODE_HEIGHT
    }
  },
  {
    selector: 'node:selected',
    style: {
      'background-color': GraphOptions.NODE_SELECTED_COLOR
    }
  }
]
