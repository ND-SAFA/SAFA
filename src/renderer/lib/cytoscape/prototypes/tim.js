import CytoscapePrototype from '.'
import edgehandles from 'cytoscape-edgehandles'
import cytoscape from 'cytoscape'
import Vue from 'vue'

import jQuery from 'jquery'
import cyqtip from 'cytoscape-qtip'
import edgeEditing from 'cytoscape-edge-editing'
import konva from 'konva'

window.$ = window.jQuery = jQuery

cyqtip(cytoscape, jQuery)
edgeEditing(cytoscape, jQuery, konva)

cytoscape.use(edgehandles)

export default class CytoscapePrototypeTIM extends CytoscapePrototype {
  constructor (container, elements, options, style, layoutTemplate) {
    super(container, elements, options, style)
    this.layoutTemplate = layoutTemplate
    this.id = 0
  }

  preLayoutHook (cy) {
    this.__addEdgeHandles(cy)
    this.__resizeNodes(cy)
  }

  layoutHook (cy) {}

  // -----------------------------------------------------------------------------
  postLayoutHook (cy) {
    this.__applyClickDragBehavior(cy)
    this.__applyCustomEvents(cy)
  }

  // ----------------------------------------------------------------------------
  // PRIVATE FUNCTIONS
  // -----------------------------------------------------------------------------
  __addEdgeHandles (cy) {
    var eh = cy.edgehandles({
      snap: true
      // complete: function (sourceNode, targetNode, addedEles) {
      //   // fired when edgehandles is done and elements are added
      //   let popper = addedEles.popper({
      //     content: () => {
      //       let div = document.createElement('div')
      //       div.innerHTML = '<form><input/></form>'
      //       document.body.appendChild(div)
      //       return div
      //     },
      //     popper: {} // my popper options here
      //   })

      //   let update = () => {
      //     popper.update()
      //   }

      //   let destroy = () => {
      //     popper.destroy()
      //   }

      //   sourceNode.on('position', update)
      //   targetNode.on('position', update)
      //   sourceNode.on('remove', destroy)
      //   targetNode.on('remove', destroy)
      //   addedEles.on('remove', destroy)
      //   cy.on('destroy', destroy)
      //   cy.on('pan zoom resize', update)
      // }
    })
    eh.enableDrawMode()
    // cy.edgeEditing({
    //   bendPositionsFunction: function (ele) {
    //     return ele.data('bendPointPositions')
    //   }
    // })
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
            name: 'Untitled',
            label: '',
            file: 'untitled.csv'
          },
          renderedPosition: {
            x: e.renderedPosition.x,
            y: e.renderedPosition.y
          }
        }])
        Vue.nonreactive(eles[0]._private.data)
        eles.qtip({
          content: {
            // text: '<div>Name:</div><form><input id="name' + eles.data('id') + '" type="text" value="' + name + '" /><button class="nameSaveButton' + eles.data('id') + '">Save</button></form><div>File Name</div><form id="eles.data("file")"><input id="file' + eles.data('id') + '" type="text" value="' + eles.data('file') + '" />  <button class="fileSaveButton' + eles.data('id') + '">Save</button></form>'
            text: '<div>Name:</div><div><input id="name' + eles.data('id') + '" type="text" value="' + eles.data('name') + '" />  <button class="nameSaveButton' + eles.data('id') + '">Save</button></div><div style="margin-top: 3px;">File Name</div><div id="eles.data("file")"><input id="file' + eles.data('id') + '" type="text" value="' + eles.data('file') + '" />  <button class="fileSaveButton' + eles.data('id') + '">Save</button></div>'
          },
          events: {
            render: function (e, api) {
              var buttonstr = '.nameSaveButton' + eles.data('id')
              var filebuttonstr = '.fileSaveButton' + eles.data('id')
              window.$(buttonstr).on('click', function () {
                var input = document.getElementById('name' + eles.data('id')).value
                console.log('node num: ', eles.data('id'))
                console.log('input for name..? ', input)
                eles.data('name', input)
              })
              window.$(filebuttonstr).on('click', function () {
                var input = document.getElementById('file' + eles.data('id')).value
                console.log('node num: ', eles.data('id'))
                console.log('input for file..? ', input)
                eles.data('file', input)
              })
              eles.on('remove', () => {
                eles.qtip('api').destroy()
              })
            }
          }
        })
        self.__clearAndApplyNodeLabels(cy, self.id)
        self.id += 1
      }
    })
    var allNodes = cy.nodes()
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

  __clearAndApplyNodeLabels (cy, id) {
    var node = cy.getElementById(id)
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

    cy.on('ehcomplete', (edge) => {
      var len = cy.edges().length
      var curr = cy.edges()[len - 1]
      console.log('info: ', curr[0])
      curr.data('file', 'undefined.csv')
      curr.data('generateLinks', false)
      Vue.nonreactive(curr[0]._private.data)
      var file = curr.data('file')
      curr.qtip({
        content: {
          text: '<div><div>Connections File Name:</div><div><input id="edgeFile' + curr.data('id') + '" type="text" value="' + file + '" /><button class="edgeFileSaveButton' + curr.data('id') + '">Save</button></div><div><span style="display: inline-block; width:80px; margin-top: 3px;">Generate Links?</span><input type="checkbox" class="generateLinks' + curr.data('id') + '"></div></div>'
        },
        position: {
          my: 'top left',
          at: 'top left'
        },
        events: {
          render: function (e, api) {
            var filebuttonstr = '.edgeFileSaveButton' + curr.data('id')
            window.$(filebuttonstr).on('click', function () {
              var input = document.getElementById('edgeFile' + curr.data('id')).value
              curr.data('file', input)
              if (curr.data('file') !== 'undefined.csv') {
                var myid = '[id = "' + curr.data('id') + '"]'
                cy.edges(myid).style('line-color', 'black')
                cy.edges(myid).style('target-arrow-color', 'black')
              }
            })
            var generatestr = '.generateLinks' + curr.data('id')
            console.log(generatestr)
            window.$(generatestr).on('click', function (e) {
              var checked = window.$(generatestr).prop('checked')
              curr.data('generateLinks', checked)
            })
            curr.on('remove', () => {
              curr.qtip('api').destroy()
            })
          }
        }
      })
      var myid = '[id = "' + curr.data('id') + '"]'
      cy.edges(myid).style('line-color', 'red')
      cy.edges(myid).style('target-arrow-color', 'red')
    })

    cy.on('destroy', () => {
      var allNodes = cy.nodes()
      allNodes.forEach(element => {
        console.log('before: ', element.qtip('api'))
        element.qtip('api').destroy()
        console.log('after: ', element.qtip('api'))
      })

      cy.elements().remove()
      console.log(cy.elements())
      console.log('getting destroyed in tim.js')
    })
  }
}
