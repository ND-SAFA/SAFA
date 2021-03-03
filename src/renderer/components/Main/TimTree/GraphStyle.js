import * as GraphOptions from '@/components/Main/SafetyArtifactTree/GraphOptions'

export default [
  {
    selector: 'edge',
    style: {
      'curve-style': GraphOptions.EDGE_CURVE_STYLE,
      'width': '1px',
      'line-color': '#000000',
      'target-arrow-shape': 'triangle'
    }
  },
  {
    selector: 'node',
    style: {
      'background-color': GraphOptions.NODE_COLOR,
      padding: GraphOptions.NODE_PADDING,
      shape: GraphOptions.NODE_SHAPE,
      width: 200,
      height: 50,
      'text-wrap': 'wrap',
      'font-size': '12px',
      'border-style': GraphOptions.NODE_BORDER_STYLE,
      'border-width': GraphOptions.NODE_BORDER_WIDTH,
      'overlay-opacity': GraphOptions.NODE_OVERLAY_OPACITY,
      'label': function (node) {
        return `${node.data('name')}\n${node.data('file')}`
      },
      'text-valign': 'center',
      'text-halign': 'center',
      'line-height': '1.3'
    }
  },
  {
    selector: 'node:selected',
    style: {
      'background-color': GraphOptions.NODE_SELECTED_COLOR
    }
  },
  {
    selector: '.eh-source',
    style: {
      'border-width': 2,
      'border-color': 'red'
    }
  },

  {
    selector: '.eh-target',
    style: {
      'border-width': 2,
      'border-color': 'red'
    }
  },
  {
    selector: '.eh-preview, .eh-ghost-edge',
    style: {
      'line-color': 'red',
      'target-arrow-color': 'red',
      'source-arrow-color': 'red'
    }
  },
  // {
  //   selector: 'source-label',
  //   style: {
  //     'label': ''
  //   }
  // },
  {
    selector: 'edge:selected',
    style: {
      'line-color': 'blue'
    }
  }
]
