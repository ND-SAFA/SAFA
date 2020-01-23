import CONFIG from 'config'

export const NODE_WIDTH = 150
export const NODE_HEIGHT = 60
export const NODE_PADDING = 2
export const NODE_COLOR = 'white'
export const NODE_SHAPE = 'rectangle'
export const NODE_BORDER_STYLE = 'solid'
export const NODE_BORDER_WIDTH = 2
export const NODE_WARNING_HEIGHT = 85
export const NODE_WARNING_COLOR = '#ffc107'
export const NODE_SELECTED_COLOR = '#ECE1FD'
export const NODE_CODE_HEIGHT = 12

export const DELTA_NODE_ADDED_COLOR = '#5eba17'
export const DELTA_NODE_ADDED_BORDER_COLOR = '#019a01'
export const DELTA_EDGE_ADDED_LINE_COLOR = '#23780a'

export const DELTA_NODE_MODIFIED_COLOR = '#2999ff'
export const DELTA_NODE_MODIFIED_BORDER_COLOR = '#2e478b'
export const DELTA_EDGE_MODIFIED_LINE_COLOR = '#2e478b'

export const DELTA_NODE_REMOVED_SHAPE = 'round-rectangle'
export const DELTA_NODE_REMOVED_COLOR = '#cf412a'
export const DELTA_NODE_REMOVED_BORDER_COLOR = '#690000'
export const DELTA_EDGE_REMOVED_LINE_COLOR = '#690000'

export const EDGE_CURVE_STYLE = 'bezier'

export const CORE_PEER_SPACING = 5
export const CORE_WHEEL_SENSITIVITY = 0.25

let ancestorExactTypes = []
let ancestorSubTypes = []
let peerNodeTypes = []
try {
  peerNodeTypes = CONFIG.get('safa_tree.peer_node_types').split(',')
  ancestorExactTypes = CONFIG.get('safa_tree.ancestor_exact_types').split(',')
  ancestorSubTypes = CONFIG.get('safa_tree.ancestor_sub_types').split(',')
} catch (e) {
  // Types Not configured in environment
}

export const CORE_PEER_NODE_TYPES = peerNodeTypes
export const CORE_ANCESTOR_EXACT_TYPES = ancestorExactTypes
export const CORE_ANCESTOR_SUB_TYPES = ancestorSubTypes
