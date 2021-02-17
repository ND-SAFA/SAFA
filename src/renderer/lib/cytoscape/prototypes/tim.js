import CytoscapePrototype from '.'
import edgehandles from 'cytoscape-edgehandles'
import cytoscape from 'cytoscape'

import jQuery from 'jquery'
import cyqtip from 'cytoscape-qtip'
cyqtip(cytoscape, jQuery)

window.$ = window.jQuery = jQuery
cytoscape.use(edgehandles)

export default class CytoscapePrototypeTIM extends CytoscapePrototype {
  constructor (container, elements, options, style, layoutTemplate) {
    super(container, elements, options, style)
    this.layoutTemplate = layoutTemplate
    this.id = 0
  }

  preLayoutHook (cy) {
    this.__addEdgeHandles(cy)
    this.__applyNodeLabels(cy)
    this.__resizeNodes(cy)
    this.__savePeerAncestorNodes(cy)
    this.__savePeerConnectingEdges(cy)
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
    this.temporaryEdges.remove()
    this.peerElements.restore()

    // Layout peer nodes closer to ancestor node
    this.__layoutPeerNodes(cy)
    this.__layoutCodeNodes(cy)
  }

  // -----------------------------------------------------------------------------
  postLayoutHook (cy) {
    this.__applyClickDragBehavior(cy)
    this.__applyPositioning(cy)
    this.__applyCustomEvents(cy)
  }

  // ----------------------------------------------------------------------------
  // PRIVATE FUNCTIONS
  // -----------------------------------------------------------------------------
  __addEdgeHandles (cy) {
    var eh = cy.edgehandles({
      snap: true,
      complete: function (sourceNode, targetNode, addedEles) {
        // fired when edgehandles is done and elements are added
        let popper = addedEles.popper({
          content: () => {
            let div = document.createElement('div')
            div.innerHTML = '<form><input/></form>'
            document.body.appendChild(div)
            return div
          },
          popper: {} // my popper options here
        })

        let update = () => {
          popper.update()
        }

        let destroy = () => {
          popper.destroy()
        }

        sourceNode.on('position', update)
        targetNode.on('position', update)
        sourceNode.on('remove', destroy)
        targetNode.on('remove', destroy)
        addedEles.on('remove', destroy)
        cy.on('destroy', destroy)
        cy.on('pan zoom resize', update)
      }
    })
    eh.enableDrawMode()
  }

  __applyClickDragBehavior (cy) {
    var self = this
    cy.on('tap', function (e) {
      var evtTarget = e.target
      if (evtTarget === cy) { // clicked on background
        var eles = cy.add([{
          group: 'nodes',
          data: {
            id: self.id,
            type: 'node',
            name: 'Hazards',
            label: '',
            file: 'hazards.csv'
          },
          renderedPosition: {
            x: e.renderedPosition.x,
            y: e.renderedPosition.y
          }
        }])
        console.log('should be adding element... qtip??? for this id: ', self.id)
        console.log('eles: ', eles.data('name'))
        var name = eles.data('name')
        eles.qtip({
          content: {
            text: '<div>Name:</div><form id="eles.data("name")"><input type="text" value="' + name + '" /><button class="nameSaveButton">Save</button></form><div>File Name</div><form id="eles.data("file")"><input type="text" value="' + eles.data('file') + '" />  <button id="saveFile">Save</button></form>' // we use $this now to reference the element that was outside qtip
          },
          style: {
            background: 'white'
          },
          events: {
            render: function (e, api) {
              window.$('.nameSaveButton').on('click', function () {
                alert('something')
                console.log('something else idk')
              })
            }
          }
        })
        self.__clearAndApplyNodeLabels(cy, self.id)
        self.id += 1
      }
    })
    var allNodes = cy.nodes()
    console.log(allNodes)
    allNodes.forEach(node => {
      const rule = cy.automove({
        nodesMatching: node.successors('node'),
        reposition: 'drag',
        dragWith: node
      })

      // ------------------------------------------------------
      // LEFT CLICK = DRAG SUB-TREE RIGHT CLICK = DRAG SINGLE
      // ------------------------------------------------------
      node.on('cxttapstart', () => {
        if (node.data().type === 'Code') {
          document.body.style.cursor = 'grabbing'
          node.lock()
        }
        rule.enable()
      })
      node.on('cxttapend free dragfree', () => {
        node.unlock()
        rule.disable()
      })
      node.on('cxtdrag', (evt) => {
        document.body.style.cursor = 'grabbing'
        const nodePosition = evt.target.renderedPosition()
        evt.target.renderedPosition({
          x: nodePosition.x + evt.originalEvent.movementX,
          y: nodePosition.y + evt.originalEvent.movementY
        })
        if (evt.target.data().type === 'Package') {
          node.emit('drag')
        }
      })
    })
  }

  // -----------------------------------------------------------------------------
  __applyNodeLabels (cy) {
    console.log('running 1!')
    cy.nodeHtmlLabel([{
      query: 'node',
      halign: 'center',
      valign: 'center',
      halignBox: 'center',
      valignBox: 'center',
      cssClass: 'safa-cy-node',
      tpl: function (data) {
        return `<div id="${data.id}_html_label">${data.label}</div>`
      }
    }, {
      query: 'node.warning',
      cssClass: 'safa-cy-node-warning',
      tpl: function (data) {
        let deltaState = ''
        if (data.delta) {
          deltaState = data.delta
        }
        return `<div id="${data.id}_html_label" class="warning-node-label ${deltaState}">${data.label}</br><div class="warning-node-info"><i class="fas fa-exclamation-triangle"></i> <b>${data.warnings[0]}</b><div></div>`
      }
    }, {
      query: 'node.warning:selected',
      tpl: function (data) {
        return `<div id="${data.id}_html_label" class="warning-node-label selected">${data.label}</br><div class="warning-node-info selected"><i class="fas fa-exclamation-triangle"></i> <b>${data.warnings[0]}</b></div></div>`
      }
    }])
  }

  __clearAndApplyNodeLabels (cy, id) {
    console.log('running 2')
    var node = cy.getElementById(id)
    const rule = cy.automove({
      nodesMatching: node.successors('node'),
      reposition: 'drag',
      dragWith: node
    })

    console.log('json: ', cy.json())

    // let popper = node.popper({
    //   content: () => {
    //     let div = document.createElement('div')
    //     div.innerHTML = '<form><input/></form>'
    //     document.body.appendChild(div)
    //     return div
    //   },
    //   popper: {} // my popper options here
    // })

    // let update = () => {
    //   popper.update()
    // }

    // node.on('position', update)
    // cy.on('pan zoom resize', update)

    // ------------------------------------------------------
    // LEFT CLICK = DRAG SUB-TREE RIGHT CLICK = DRAG SINGLE
    // ------------------------------------------------------
    node.on('cxttapstart', () => {
      if (node.data().type === 'Code') {
        document.body.style.cursor = 'grabbing'
        node.lock()
      }
      rule.enable()
    })
    node.on('cxttapend free dragfree', () => {
      node.unlock()
      rule.disable()
    })
    node.on('cxtdrag', (evt) => {
      document.body.style.cursor = 'grabbing'
      const nodePosition = evt.target.renderedPosition()
      evt.target.renderedPosition({
        x: nodePosition.x + evt.originalEvent.movementX,
        y: nodePosition.y + evt.originalEvent.movementY
      })
      if (evt.target.data().type === 'Package') {
        node.emit('drag')
      }
    })
  }

  // -----------------------------------------------------------------------------
  __resizeNodes (cy) {
    process.nextTick(() => {
      const nodes = cy.nodes('[type!="Code"]')
      for (let i = 0; i < nodes.length; i++) {
        let ele = document.getElementById(nodes[i].data().id + '_html_label')
        if (ele !== null) {
          nodes[i].css('height', ele.clientHeight)
          nodes[i].css('width', ele.clientWidth)
        }
      }
    })
  }

  // -----------------------------------------------------------------------------
  __applyCustomEvents (cy) {
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

    cy.on('drag', 'node', () => {
      document.body.style.cursor = 'grabbing'
    })

    cy.on('dragfree free', 'node', () => {
      document.body.style.cursor = 'auto'
    })
  }

  // -----------------------------------------------------------------------------
  __applyPositioning (cy) {
    cy.center(cy.nodes().roots().first())
    cy.panBy({ y: -(cy.size().height / 2 - this.options.NODE_HEIGHT) })
  }

  // -----------------------------------------------------------------------------
  __layoutCodeNodes (cy) {
    process.nextTick((self = this) => {
      for (let i = 0; i < self.packageNodes.length; i++) {
        // Align each code node under package node
        const node = self.packageNodes[i]
        const codeNodes = node.outgoers('node')
        codeNodes.forEach((codeNode, index) => {
          // Toggle height change
          codeNode.css('width', node.width())
          codeNode.toggleClass('code-node')
          codeNode.position('x', node.position('x'))
          const yPosition = node.position('y') + node.outerHeight() / 2 + codeNode.outerHeight() / 2 + codeNode.outerHeight() * index - self.options.NODE_BORDER_WIDTH * (index + 1)
          codeNode.position('y', yPosition)
          // Hide any edges so they don't occlude the nodes
          codeNode.connectedEdges().first().style('visibility', 'hidden')
        })
      }
    })
  }

  // -----------------------------------------------------------------------------
  __layoutPeerNodes (cy) {
    for (let i = 0; i < this.peerNodes.length; i++) {
      const ancestorNode = this.peerNodes[i].incomers('node').first()
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
  // needs to be called after saving peer nodes
  __savePeerConnectingEdges (cy) {
    this.temporaryEdges = cy.collection()
    for (let i = 0; i < this.peerNodes.length; i++) {
      // Get parent node
      const ancestor = this.peerNodes[i].incomers('node')
      // Get all outgoing edges
      const childEdges = this.peerNodes[i].outgoers('edge')
      for (let j = 0; j < childEdges.length; j++) {
        // Create new edge with parent as source and current edge target
        const newEdge = cy.add({
          data: {
            source: ancestor.id(),
            target: childEdges[j].target().id()
          }
        })
        // Add new edge to the collection of temporary edges
        this.temporaryEdges = this.temporaryEdges.union(newEdge)
      }
    }
  }

  // -----------------------------------------------------------------------------
  __savePeerAncestorNodes (cy) {
    // Valid peer node types
    const peerNodeTypes = this.options.CORE_PEER_NODE_TYPES
    const peerSelector = peerNodeTypes.map(peerType => `[type="${peerType}"]`).join(',')
    // Get nodes that should be peers
    this.peerNodes = cy.nodes(peerSelector)
    // Valid ancestor node types
    const ancestorExactTypes = this.options.CORE_ANCESTOR_EXACT_TYPES
    // Valid ancestor node types that contain the following text
    const ancestorSubTypes = this.options.CORE_ANCESTOR_SUB_TYPES
    const ancestorNodeTypes = ancestorExactTypes.map(exactType => `node[type="${exactType}"]`).concat(ancestorSubTypes.map(subType => `node[type*="${subType}"]`))
    const ancestorSelector = ancestorNodeTypes.join(',')
    // Get nodes connected to above peer nodes
    this.ancestorNodes = this.peerNodes.incomers(ancestorSelector)
    // Save the number of peers in the ancestor node for layout purposes
    for (let i = 0; i < this.ancestorNodes.length; i++) {
      const peers = this.ancestorNodes[i].outgoers().intersection(this.peerNodes)
      for (let j = 0; j < peers.length; j++) {
        // Save the corresponding index in each peer node
        peers[j].scratch('peerIndex', j)
      }
      const numPeerNodes = peers.length
      this.ancestorNodes[i].scratch('numPeerNodes', numPeerNodes)
      this.ancestorNodes[i].style('width', this.options.NODE_WIDTH + (this.ancestorNodes[i].outerWidth() + this.options.CORE_PEER_SPACING) * (numPeerNodes + 1))
    }
    this.peerElements = this.peerNodes.union(this.peerNodes.connectedEdges()).remove()
  }

  // -----------------------------------------------------------------------------
  __savePackageNodes (cy) {
    // Get all package nodes
    this.packageNodes = cy.nodes('[type="Package"]')
    this.packageNodes.forEach(packageNode => {
      // Get number of code nodes in each package
      const numCodeNodes = packageNode.outgoers('edge').length
      // Calculate and set total height of package node
      packageNode.style('height', packageNode.outerHeight() + numCodeNodes * (this.options.NODE_CODE_HEIGHT + 2 * this.options.NODE_PADDING - this.options.NODE_BORDER_WIDTH))
    })

    // Remove code nodes and edges
    this.codeNodes = cy.nodes('[type="Code"]')
    this.codeElements = this.codeNodes.union(this.codeNodes.connectedEdges()).remove()
  }
}
