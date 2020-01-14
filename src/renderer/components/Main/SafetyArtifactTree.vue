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
import { mapGetters } from 'vuex'
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

  computed: {
    ...mapGetters('projects.module', ['getHazardTree']),
    treeElements () {
      if (this.getHazardTree) {
        return JSON.parse(JSON.stringify(this.getHazardTree))
      } else {
        return []
      }
    }
  },

  data () {
    return {
      cytoscapeProto: Object()
    }
  },

  mounted () {
    this.makeGraph(this.$refs.cy)
  },

  methods: {
    makeGraph (container) {
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
        direction: L.DIRECTION.UP,
        fixedAlignment: L.FIXED_ALIGNMENT.BALANCED,
        layoutHierarchy: true,
        nodeLayering: L.NODE_LAYERING.NETWORK_SIMPLEX,
        nodePlacement: L.NODE_PLACEMENT.LINEAR_SEGMENTS
      })

      this.cytoscapeProto = new CytoscapePrototypeSAFA(container, this.treeElements, GraphOptions, GraphStyle, klayLayoutTemplate, badgeFactory)
      this.cytoscapeProto.run()
    }
  }
}
</script>

<style scoped>

</style>
