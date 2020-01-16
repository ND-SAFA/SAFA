import CytoscapePrototype from '.'
import cytoscape from 'cytoscape'
import klay from 'cytoscape-klay'
import nodeHtmlLabel from 'cytoscape-node-html-label'
import popper from 'cytoscape-popper'
import automove from 'cytoscape-automove'

nodeHtmlLabel(cytoscape)
cytoscape.use(klay)
cytoscape.use(popper)
cytoscape.use(automove)

export default class CytoscapePrototypeSAFA extends CytoscapePrototype {
  constructor (container, elements, options, style, layoutTemplate, badgeFactory) {
    super(container, elements, options, style)
    this.layoutTemplate = layoutTemplate
    this.badgeFactory = badgeFactory
    this.badges = []
  }

  preLayoutHook (cy) {
    while (this.badges.length) {
      const badge = this.badges.pop()
      badge.destroy()
    }
    this.__savePeerNodes(cy)
    this.__saveAncestorNodes(cy)
    this.__savePackageNodes(cy)
  }

  // -----------------------------------------------------------------------------
  layoutHook (cy) {
    this.layoutTemplate.makeLayout(cy).run()

    this.__layoutAncestorNodes(cy)

    // Reset package nodes height
    this.packageNodes.removeStyle('height')

    // Restore code nodes
    this.codeElements.restore()
    this.peerElements.restore()

    // Layout peer nodes closer to ancestor node
    this.__layoutPeerNodes(cy)
    this.__layoutCodeNodes(cy)
  }

  // -----------------------------------------------------------------------------
  postLayoutHook (cy) {
    this.__applyClickDragBehavior(cy)
    this.__applyBadges(cy)
    this.__applyNodeLabels(cy)
    this.__applyCustomEvents(cy)
    this.__applyPositioning(cy)
  }

  // ----------------------------------------------------------------------------
  // PRIVATE FUNCTIONS
  // -----------------------------------------------------------------------------
  __applyClickDragBehavior (cy) {
    const allNodes = cy.nodes()
    allNodes.forEach(node => {
      const rule = cy.automove({
        nodesMatching: node.predecessors('node'),
        reposition: 'drag',
        dragWith: node
      })

      // ------------------------------------------------------
      // LEFT CLICK = DRAG SUB-TREE RIGHT CLICK = DRAG SINGLE
      // ------------------------------------------------------
      node.on('tapstart', () => {
        if (node.data().type === 'Code') {
          node.lock()
        }
        rule.enable()
      })
      node.on('tapend', () => {
        node.unlock()
        rule.disable()
      })
      node.on('cxttapstart', (evt) => {
        if (node.data().type === 'Code') {
          node.lock()
        }
        if (evt.target.data().type === 'Package') {
          rule.enable()
          node.emit('grab')
        }
      })
      node.on('cxttapend', () => {
        node.unlock()
        node.emit('free')
        rule.disable()
      })
      node.on('cxtdrag', (evt) => {
        evt.target.renderedPosition(evt.renderedPosition)
        if (evt.target.data().type === 'Package') {
          node.emit('drag')
        }
      })
    })
  }

  // -----------------------------------------------------------------------------
  __applyBadges (cy) {
    cy.nodes('.modified,.added,.removed').forEach(node => {
      // Find matching class
      const classes = node.classes()
      let theme = 'modified'
      if (classes.find(element => element === 'added')) {
        theme = 'added'
      } else if (classes.find(element => element === 'removed')) {
        theme = 'removed'
      }
      this.badges.push(this.badgeFactory.getBadgeForTemplate(node, theme))
    })
  }

  // -----------------------------------------------------------------------------
  __applyNodeLabels (cy) {
    cy.nodeHtmlLabel([{
      query: 'node',
      halign: 'center',
      valign: 'center',
      halignBox: 'center',
      valignBox: 'center',
      cssClass: 'safa-cy-node',
      tpl: function (data) {
        return data.label
      }
    }, {
      query: 'node.warning',
      cssClass: 'safa-cy-node-warning',
      tpl: function (data) {
        let deltaState = ''
        if (data.delta) {
          deltaState = data.delta
        }
        return `<div class="warning-node-label ${deltaState}">${data.label}</div></br><div class="warning-node-info"><i class="fas fa-exclamation-triangle"></i> <b>WARNING</b><div>${data.warnings[0]}</div></div>`
      }
    }, {
      query: 'node.warning:selected',
      tpl: function (data) {
        return `<div class="warning-node-label selected">${data.label}</div></br><div class="warning-node-info selected"><i class="fas fa-exclamation-triangle"></i> <b>WARNING</b><div>${data.warnings[0]}</div></div>`
      }
    }])
  }

  // -----------------------------------------------------------------------------
  __applyCustomEvents (cy) {
    // cy.on('unselect', removeNodeDetails)

    // cy.on('select', addNodeDetails)

    cy.on('mouseover', 'node', () => {
      document.body.style.cursor = 'pointer'
    })

    cy.on('mouseout', 'node', () => {
      document.body.style.cursor = 'auto'
    })

    cy.on('resize', (e) => {
      const newSize = { w: cy.container().clientWidth, h: cy.container().clientHeight }
      const widthChange = newSize.w - cy.oldSize.w
      const heightChange = newSize.h - cy.oldSize.h
      const currentPan = cy.pan()
      const newPan = { x: currentPan.x + (widthChange * 0.5), y: currentPan.y + (heightChange * 0.5) }
      cy.pan(newPan)
      cy.oldSize = newSize
    })
  }

  // -----------------------------------------------------------------------------
  __applyPositioning (cy) {
    cy.center(cy.nodes().leaves().first())
    cy.panBy({ y: -(cy.size().height / 2 - this.options.NODE_HEIGHT) })
  }

  // -----------------------------------------------------------------------------
  __layoutCodeNodes (cy) {
    for (let i = 0; i < this.packageNodes.length; i++) {
      // Align each code node under package node
      const node = this.packageNodes[i]
      const codeNodes = node.incomers('node')
      codeNodes.forEach((codeNode, index) => {
        // Toggle height change
        codeNode.toggleClass('code-node')
        codeNode.position('x', node.position('x'))
        const yPosition = node.position('y') + node.outerHeight() / 2 + codeNode.outerHeight() / 2 + codeNode.outerHeight() * index - this.options.NODE_BORDER_WIDTH * (index + 1)
        codeNode.position('y', yPosition)
        // Hide any edges so they don't occlude the nodes
        codeNode.connectedEdges().first().style('visibility', 'hidden')
      })
    }
  }

  // -----------------------------------------------------------------------------
  __layoutPeerNodes (cy) {
    for (let i = 0; i < this.peerNodes.length; i++) {
      const ancestorNode = this.peerNodes[i].outgoers('node').first()
      if ((this.peerNodes[i].scratch('peerIndex') + 1) % 2) {
        this.peerNodes[i].position('x', ancestorNode.position('x') + (this.peerNodes[i].outerWidth() + this.options.CORE_PEER_SPACING) * (this.peerNodes[i].scratch('peerIndex') + 1))
      } else {
        this.peerNodes[i].position('x', ancestorNode.position('x') - (this.peerNodes[i].outerWidth() + this.options.CORE_PEER_SPACING) * (this.peerNodes[i].scratch('peerIndex')))
      }
      this.peerNodes[i].position('y', ancestorNode.position('y'))
    }
  }

  // -----------------------------------------------------------------------------
  __layoutAncestorNodes (cy) {
    this.ancestorNodes.removeStyle('width')
    for (let i = 0; i < this.ancestorNodes.length; i++) {
      this.ancestorNodes[i].shift('x', this.ancestorNodes[i].outerWidth() + this.options.CORE_PEER_SPACING)
    }
  }

  // -----------------------------------------------------------------------------
  __savePeerNodes (cy) {
    // Valid peer node types
    const peerNodeTypes = this.options.CORE_PEER_NODE_TYPES
    const peerSelector = peerNodeTypes.map(peerType => `[type="${peerType}"]`).join(',')
    // Get nodes that should be peers
    this.peerNodes = cy.nodes(peerSelector)
    this.peerElements = this.peerNodes.union(this.peerNodes.connectedEdges()).remove()
  }

  // -----------------------------------------------------------------------------
  __saveAncestorNodes (cy) {
    // Valid ancestor node types
    const ancestorExactTypes = this.options.CORE_ANCESTOR_EXACT_TYPES
    // Valid ancestor node types that contain the following text
    const ancestorSubTypes = this.options.CORE_ANCESTOR_SUB_TYPES
    const ancestorNodeTypes = ancestorExactTypes.map(exactType => `node[type="${exactType}"]`).concat(ancestorSubTypes.map(subType => `node[type*="${subType}"]`))
    const ancestorSelector = ancestorNodeTypes.join(',')
    // Get nodes connected to above peer nodes
    this.ancestorNodes = this.peerNodes.outgoers(ancestorSelector)
    // Save the number of peers in the ancestor node for layout purposes
    for (let i = 0; i < this.ancestorNodes.length; i++) {
      const peers = this.ancestorNodes[i].incomers().intersection(this.peerNodes)
      for (let j = 0; j < peers.length; j++) {
        // Save the corresponding index in each peer node
        peers[j].scratch('peerIndex', j)
      }
      const numPeerNodes = peers.length
      this.ancestorNodes[i].scratch('numPeerNodes', numPeerNodes)
      this.ancestorNodes[i].style('width', this.options.NODE_WIDTH + (this.ancestorNodes[i].outerWidth() + this.options.CORE_PEER_SPACING) * (numPeerNodes + 1))
    }
  }

  // -----------------------------------------------------------------------------
  __savePackageNodes (cy) {
    // Get all package nodes
    this.packageNodes = cy.nodes('[type="Package"]')
    this.packageNodes.forEach(packageNode => {
      // Get number of code nodes in each package
      const numCodeNodes = packageNode.incomers('edge').length
      // Calculate and set total height of package node
      packageNode.style('height', packageNode.outerHeight() + numCodeNodes * (this.options.NODE_CODE_HEIGHT + 2 * this.options.NODE_PADDING - this.options.NODE_BORDER_WIDTH))
    })

    // Remove code nodes and edges
    this.codeNodes = cy.nodes('[type="Code"]')
    this.codeElements = this.codeNodes.union(this.codeNodes.connectedEdges()).remove()
  }
}
