export default class LayoutBaseTemplate {
  __name = 'BaseLayout'

  constructor (zoom) {
    this.zoom = zoom
  }

  get name () {
    return this.__name
  }

  factory (cy) {
    const { name, zoom } = this
    return cy.layout({name, zoom})
  }
}
