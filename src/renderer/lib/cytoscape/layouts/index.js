export default class LayoutBaseTemplate {
  __name = 'BaseLayout'

  constructor (zoom, pan) {
    this.zoom = zoom
    this.pan = pan
  }

  get name () {
    return this.__name
  }

  factory (cy) {
    const { name, zoom, pan } = this
    return cy.layout({name, zoom, pan})
  }
}
