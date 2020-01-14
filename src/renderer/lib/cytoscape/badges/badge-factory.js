import BadgeTemplate from './badge-template'

export default class BadgeFactory {
  setTemplate (name, badgeTemplate) {
    if (!(badgeTemplate instanceof BadgeTemplate)) {
      throw new Error(`Expected a BadgeTemplate but got ${typeof (badgeTemplate)} of ${badgeTemplate.constructor}`)
    }

    this[name] = badgeTemplate
  }

  getBadgeForTemplate (node, templateName) {
    const badgeTemplate = this[templateName]
    if (badgeTemplate === undefined || badgeTemplate === null) {
      throw new Error('Badge template not initialized')
    }

    return badgeTemplate.fabricateFor(node)
  }
}
