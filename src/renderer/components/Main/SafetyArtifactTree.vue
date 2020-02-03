<template>
  <div id="center-panel" role="tabpanel" aria-labelledby="artifact-tree-tab" class="fade col show active graph-view p-0">
    <div id="loading-graph-spinner" style="display:none">
      <div class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
    <div id="cy-error" class="alert alert-warning alert-dismissible fade show" role="alert" style="display:none">
      <span id="cy-error-text">Problem Rendering the Graph.</span>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div id="cy-parent">
      <div id="cy" ref="cy"></div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import AppMenu from '@/menu'
import Vue from 'vue'
import BadgeTemplate from '@/lib/cytoscape/badges/badge-template'
import BadgeFactory from '@/lib/cytoscape/badges/badge-factory'
import * as GraphOptions from '@/components/Main/SafetyArtifactTree/GraphOptions'
import GraphStyle from '@/components/Main/SafetyArtifactTree/GraphStyle'
import CytoscapePrototypeSAFA from '@/lib/cytoscape/prototypes/cytoscape-prototype-safa'
import LayoutTemplateKlay from '@/lib/cytoscape/layouts/layout-template-klay'

const L = LayoutTemplateKlay
const B = BadgeTemplate

export default {
  name: 'SafetyArtifactTree',
  props: ['treeId'],
  computed: {
    ...mapGetters('projects.module', ['getHazardTree', 'getSafetyArtifactTree']),
    treeElements: function () {
      if (this.treeId) {
        return JSON.parse(JSON.stringify(this.getSafetyArtifactTree))
      }
      return JSON.parse(JSON.stringify(this.getHazardTree))
    }
  },
  watch: {
    treeId: async function (newTreeId) {
      if (this.treeId) {
        await this.fetchSafetyArtifactTree(newTreeId)
      }
      this.makeGraph(this.$refs.cy)
    }
  },

  data () {
    return {
      cytoscapeProto: Object()
    }
  },

  created () {
    AppMenu.findMenuItemById('view.graph_zoom_in').click = this.graphZoomIn.bind(this)
    AppMenu.findMenuItemById('view.graph_zoom_out').click = this.graphZoomOut.bind(this)
    AppMenu.setApplicationMenu()
  },

  mounted () {
    this.makeGraph(this.$refs.cy)
  },

  methods: {
    ...mapActions('projects.module', ['fetchSafetyArtifactTree']),
    makeGraph: async function (container) {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.destroy()
      }

      const badgeTemplate = {
        trigger: B.TRIGGER.MANUAL,
        placement: B.PLACEMENT.BOTTOM_END,
        hideOnClick: false,
        sticky: true,
        offset: '20, -15',
        showOnInit: true,
        animateFill: false,
        zIndex: 1,
        ignoreAttributes: true,
        badgeSize: B.SIZE.SMALL
      }

      const badgeFactory = new BadgeFactory()
      badgeFactory.setTemplate('added', new BadgeTemplate(Object.assign({}, {theme: 'added'}, badgeTemplate)))
      badgeFactory.setTemplate('modified', new BadgeTemplate(Object.assign({}, {theme: 'modified'}, badgeTemplate)))
      badgeFactory.setTemplate('removed', new BadgeTemplate(Object.assign({}, {theme: 'removed'}, badgeTemplate)))

      const klayLayoutTemplate = new LayoutTemplateKlay({
        zoom: 1.12,
        spacing: 15,
        direction: L.DIRECTION.DOWN,
        fixedAlignment: L.FIXED_ALIGNMENT.BALANCED,
        layoutHierarchy: true,
        nodeLayering: L.NODE_LAYERING.NETWORK_SIMPLEX,
        nodePlacement: L.NODE_PLACEMENT.LINEAR_SEGMENTS
      })

      this.cytoscapeProto = new CytoscapePrototypeSAFA(container, this.treeElements, GraphOptions, GraphStyle, klayLayoutTemplate, badgeFactory)
      this.cytoscapeProto.run()

      this.cytoscapeProto.cy.on('unselect-node', this.$emit.bind(this, 'unselect-node'))
    },
    graphZoomIn () {
      console.log('graphZoomIn()')
    },
    graphZoomOut () {
      console.log('graphZoomOut()')
    }
  }
}
</script>

<style scoped>

</style>
