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
import CytoscapePrototypeDelta from '@/lib/cytoscape/prototypes/cytoscape-prototype-delta'
import LayoutTemplateKlay from '@/lib/cytoscape/layouts/layout-template-klay'

const L = LayoutTemplateKlay
const B = BadgeTemplate

export default {
  name: 'DeltaTree',
  props: ['treeId'],

  computed: {
    ...mapGetters('projects.module', ['getDeltaTrees']),
    ...mapGetters('app.module', ['getDeltaState']),
    treeElements () {
      return JSON.parse(JSON.stringify(this.getDeltaTrees))
    },
    deltaChanged () {
      return this.getDeltaState.changed
    }
  },

  watch: {
    treeId () {
      this.renderGraph()
    },
    deltaChanged () {
      this.renderGraph()
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
    this.renderDeltaTree(this.$refs.cy)
  },

  methods: {
    ...mapActions('projects.module', ['fetchDeltaTrees']),

    async renderDeltaTree (container) {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.destroy()
      }

      const { baseline, current } = this.getDeltaState
      await this.fetchDeltaTrees({treeId: this.treeId, baseline, current})

      const layout = new LayoutTemplateKlay({
        zoom: 1.12,
        spacing: 15,
        direction: L.DIRECTION.DOWN,
        fixedAlignment: L.FIXED_ALIGNMENT.BALANCED,
        layoutHierarchy: true,
        nodeLayering: L.NODE_LAYERING.NETWORK_SIMPLEX,
        nodePlacement: L.NODE_PLACEMENT.LINEAR_SEGMENTS
      })

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

      const elements = CytoscapePrototypeDelta.calculateDeltas(this.treeElements, baseline, current)

      this.cytoscapeProto = new CytoscapePrototypeDelta(container, elements, GraphOptions, GraphStyle, layout, badgeFactory)
      this.cytoscapeProto.run()
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
