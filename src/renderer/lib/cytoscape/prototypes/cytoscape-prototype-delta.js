import CytoscapePrototypeSAFA from './cytoscape-prototype-safa'
import cytoscape from 'cytoscape'
import popper from 'cytoscape-popper'

cytoscape.use(popper)

export default class CytoscapePrototypeDelta extends CytoscapePrototypeSAFA {
  constructor (container, elements, options, style, layoutTemplate, badgeFactory) {
    super(container, elements, options, style, layoutTemplate)
    this.badgeFactory = badgeFactory
    this.badges = []
  }

  // -----------------------------------------------------------------------------
  postLayoutHook (cy) {
    super.postLayoutHook(cy)
    this.__applyBadges(cy)
  }

  // -----------------------------------------------------------------------------
  destroy () {
    super.destroy()
    while (this.badges.length) {
      const badge = this.badges.pop()
      badge.destroy()
    }
  }

  // -----------------------------------------------------------------------------
  static calculateDeltas (graphs, baseline, current) {
    const cytos = graphs.map(elements => cytoscape({ elements: elements }))
    let changeCounter = 1
    // Intersection between current and baseline
    const intersection = cytos[0].elements().intersection(cytos[1].elements())
    // Tag elements as modified
    if (current !== baseline) {
      intersection.nodes().forEach(node => {
        if (node.data('modified')) {
          node.addClass('modified')
          // Add modified styling to any connected edges
          const edges = node.outgoers('edge')
          edges.forEach(edge => edge.addClass('modified'))
          node.data('delta', 'modified')
          node.data('changeIndex', changeCounter++)
        }
      })
    }
    // Diff between current and intersection
    const added = intersection.symmetricDifference(cytos[0].elements())
    // Tag elements as added
    added.addClass('added')
    added.forEach(node => {
      node.data('delta', 'added')
      node.data('changeIndex', changeCounter++)
    })
    // Diff between baseline and intersection
    const removed = intersection.symmetricDifference(cytos[1].elements())
    // Tag elements as removed
    removed.addClass('removed')
    removed.forEach(node => {
      node.data('delta', 'removed')
      node.data('changeIndex', changeCounter++)
    })
    // Join intersection, "added" and "removed" graphs
    const union = intersection.union(added).union(removed)
    // return plain JSON
    return union.jsons()
  }

  // ----------------------------------------------------------------------------
  // PRIVATE FUNCTIONS
  // -----------------------------------------------------------------------------

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
}
