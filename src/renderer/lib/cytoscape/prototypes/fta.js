import CytoscapePrototype from '.'

export default class CytoscapePrototypeFTA extends CytoscapePrototype {
  constructor (container, elements, options, style, layoutTemplate) {
    super(container, elements, options, style)
    this.layoutTemplate = layoutTemplate
  }
}
