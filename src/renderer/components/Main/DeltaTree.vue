<template>
  <div id="center-panel" role="tabpanel" aria-labelledby="artifact-tree-tab" class="fade col show active graph-view p-0">
    <div id="loading-graph-spinner" v-show="showSpinner">
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
import CytoscapePrototypeDelta from '@/lib/cytoscape/prototypes/delta'
import LayoutTemplateKlay from '@/lib/cytoscape/layouts/layout-template-klay'

const L = LayoutTemplateKlay
const B = BadgeTemplate

export default {
  name: 'DeltaTree',
  props: {
    update: Number,
    resize: Number,
    treeId: String,
    isFetchingFromServer: Boolean
  },

  computed: {
    ...mapGetters('projects.module', ['getDeltaTrees']),
    ...mapGetters('app.module', ['getDeltaState']),
    treeElements () {
      return JSON.parse(JSON.stringify(this.getDeltaTrees))
    },
    deltaChanged () {
      return this.getDeltaState.changed
    },
    showSpinner () {
      return this.isFetchingFromServer || this.isUpdating
    }
  },

  watch: {
    treeId () {
      this.renderDeltaTree(this.$refs.cy)
    },
    deltaChanged () {
      this.renderDeltaTree(this.$refs.cy)
    },
    resize () {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.cy.resize()
      }
    },
    update () {
      this.renderDeltaTree(this.$refs.cy)
    }
  },

  data () {
    return {
      cytoscapeProto: Object(),
      isUpdating: false
    }
  },

  created () {
    AppMenu.findMenuItemById('view.graph_zoom_in').click = this.graphZoomIn.bind(this)
    AppMenu.findMenuItemById('view.graph_zoom_out').click = this.graphZoomOut.bind(this)
    AppMenu.setApplicationMenu()
  },

  mounted () {
    this.setDeltaTreeChangeLog({})
    this.renderDeltaTree(this.$refs.cy)
  },

  beforeDestroy () {
    if (!Vue.isEmpty(this.cytoscapeProto)) {
      this.cytoscapeProto.destroy()
    }
  },

  methods: {
    ...mapActions('projects.module', ['fetchDeltaTrees']),
    ...mapActions('app.module', ['setDeltaTreeChangeLog', 'setSelectedArtifact']),

    async renderDeltaTree (container) {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.destroy()
        this.setSelectedArtifact({})
      }

      const { baseline, current } = this.getDeltaState
      try {
        this.isUpdating = true
        await this.fetchDeltaTrees({treeId: this.treeId, baseline, current})

        const layout = new LayoutTemplateKlay({
          zoom: 1.12,
          spacing: 1,
          direction: L.DIRECTION.DOWN,
          fixedAlignment: L.FIXED_ALIGNMENT.BALANCED,
          layoutHierarchy: true,
          nodeLayering: L.NODE_LAYERING.NETWORK_SIMPLEX,
          nodePlacement: L.NODE_PLACEMENT.BRANDES_KOEPF,
          inLayerSpacingFactor: 0.4,
          thoroughness: 10
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

        const elements = CytoscapePrototypeDelta.calculateDelta(this.treeElements, baseline, current)
        const changeLog = CytoscapePrototypeDelta.calculateChangeLog(elements)
        this.setDeltaTreeChangeLog(changeLog)

        this.cytoscapeProto = new CytoscapePrototypeDelta(container, elements, GraphOptions, GraphStyle, layout, badgeFactory)
        await this.cytoscapeProto.run()

        const component = this
        this.cytoscapeProto.cy.on('select', 'node', evt => {
          component.$emit('select:node')
          component.setSelectedArtifact(evt.target.data())
        })
        this.cytoscapeProto.cy.on('click', () => this.setSelectedArtifact({}))
      } catch (e) {
        // TODO(Adam): handle error
      }
      this.isUpdating = false
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
  #loading-graph-spinner {
    position: relative;
    width: 100%;
    height: 100%;
    background: white;
    z-index: 1000;
  }
</style>
