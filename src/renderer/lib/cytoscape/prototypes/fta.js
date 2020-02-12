import CytoscapePrototype from '.'

const NOOP = () => null

export default class CytoscapePrototypeFTA extends CytoscapePrototype {
  constructor (container, elements, options, style, layoutTemplate) {
    super(container, elements, options, style)
    this.layoutTemplate = layoutTemplate
  }

  // -----------------------------------------------------------------------------
  preLayoutHook () {
    NOOP()
  }

  // -----------------------------------------------------------------------------
  layoutHook (cy) {
    const excludeWarnings = cy.elements().not(cy.nodes('.gate-node'))
    this.layoutTemplate.makeLayout(excludeWarnings).run()
  }

  // -----------------------------------------------------------------------------
  postLayoutHook (cy) {
    this.__applyClickDragBehavior(cy)
    this.__applyNodeLabels(cy)
    this.__applyPositioning(cy)
    this.__applyCustomEvents(cy)
  }

  // ----------------------------------------------------------------------------
  // PRIVATE FUNCTIONS
  // -----------------------------------------------------------------------------
  __applyClickDragBehavior (cy) {
    const allNodes = cy.nodes()
    allNodes.forEach(node => {
      const rule = cy.automove({
        nodesMatching: node.successors('node'),
        reposition: 'drag',
        dragWith: node
      })

      // ------------------------------------------------------
      // LEFT CLICK = DRAG SUB-TREE RIGHT CLICK = DRAG SINGLE
      // ------------------------------------------------------
      node.on('tapstart', () => {
        if (node.data().type === 'Code') {
          document.body.style.cursor = 'grabbing'
          node.lock()
        }
        rule.enable()
      })
      node.on('tapend free dragfree', () => {
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
    cy.nodes('.logical-gate').forEach(gate => {
      const id = gate.id()
      gate.ungrabify()
      gate.connectedEdges().forEach(edge => {
        if (edge.data().target === id) {
          const parent = cy.nodes(`[id="${edge.data().source}"]`)
          const pos = parent.position()
          let yOffset = 62
          if (gate.hasClass('stop-gate')) {
            yOffset = 52
          }
          gate.position({ x: pos.x, y: pos.y + yOffset })
        }
      })
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
        return data.name || ''
      }
    }, {
      query: 'node.or-gate',
      cssClass: 'safa-cy-logical-gate',
      tpl: function (data) {
        return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="2rem" height="2rem" viewBox="-0.5 -2.5 91 108" style="background-color: rgba(255, 255, 255, 0);"><defs/><g><path d="M -2.5 2.5 Q 92.5 2.5 92.5 47.5 Q 92.5 92.5 -2.5 92.5 Q 45 47.5 -2.5 2.5 Z" fill="#ffffff" stroke="#000000" stroke-miterlimit="10" stroke-width="6" transform="rotate(-90,45,47.5)" pointer-events="all"/></g></svg>'
      }
    }, {
      query: 'node.and-gate',
      cssClass: 'safa-cy-logical-gate',
      tpl: function (data) {
        return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="2rem" height="2rem" viewBox="-2.5 -2.0 85 85"><defs/><g><path d="M 0 0 Q 80 0 80 40 Q 80 80 0 80 Z" fill="#ffffff" stroke="#000000" stroke-width="5" stroke-miterlimit="10" transform="rotate(-90 40 40)" pointer-events="all"/></g></svg>'
      }
    }, {
      query: 'node.stop-gate',
      cssClass: 'safa-cy-logical-gate',
      tpl: function (data) {
        return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="2rem" height="2rem" viewBox="-2.5 -0.5 85 85"><defs/><g><ellipse cx="40" cy="40" rx="40" ry="40" fill="#ffffff" stroke-width="5" stroke="#000000" pointer-events="all"/></g></svg>'
      }
    }])
  }

  // -----------------------------------------------------------------------------
  __applyCustomEvents (cy) {
    cy.on('mouseover', 'node', () => {
      document.body.style.cursor = 'pointer'
    })

    cy.on('mouseout', 'node', () => {
      document.body.style.cursor = 'auto'
    })

    cy.on('resize', () => {
      const newSize = { w: cy.container().clientWidth, h: cy.container().clientHeight }
      const widthChange = newSize.w - cy.oldSize.w
      const currentPan = cy.pan()
      cy.pan({ x: currentPan.x + (widthChange * 0.5), y: 100 })
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
}
