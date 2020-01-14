import cytoscape from 'cytoscape'

export default class CytoscapePrototype {
  constructor (container, elements, options, style) {
    this.container = container
    this.elements = elements
    this.style = style
    this.options = options
  }

  preLayoutHook () {
    throw new Error(`${this.prototype} extends CytoscapePrototype but does not implement preLayoutHook()`)
  }

  layoutHook () {
    throw new Error(`${this.prototype} extends CytoscapePrototype but does not implement layoutHook()`)
  }

  postLayoutHook () {
    throw new Error(`${this.prototype} extends CytoscapePrototype but does not implement postLayoutHook()`)
  }

  run () {
    const self = this
    const cy = cytoscape({
      container: this.container,
      elements: this.elements,
      wheelSensitivity: this.options.CORE_WHEEL_SENSITIVITY,
      style: this.style,
      ready: function () {
        const cy = this
        cy.oldSize = { w: cy.container().clientWidth, h: cy.container().clientHeight }
        self.preLayoutHook(cy)
        self.layoutHook(cy)
      }
    })
    self.postLayoutHook(cy)
    this.cy = cy
    return cy
  }
}
