import Vue from 'vue'

export default {
  methods: {
    __zoom (increment) {
      if (Vue.isEmpty(this.cytoscapeProto)) {
        return
      }
      const cy = this.cytoscapeProto.cy
      cy.zoom({
        level: cy.zoom() * Math.pow(10, increment),
        renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 }
      })
    },

    graphZoomIn () {
      this.__zoom(0.005)
    },

    graphZoomOut () {
      this.__zoom(-0.005)
    }
  }
}
