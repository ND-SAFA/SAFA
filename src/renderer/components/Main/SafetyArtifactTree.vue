<template>
  <div id="center-panel" role="tabpanel" aria-labelledby="artifact-tree-tab" aria-hidden="false" class="col show active graph-view p-0">
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
import config from 'config'
import { mapActions, mapGetters } from 'vuex'
import AppMenu from '@/menu'
import Vue from 'vue'
import CytoscapeMixin from '@/mixins/cytoscape-graph'
import * as GraphOptions from '@/components/Main/SafetyArtifactTree/GraphOptions'
import GraphStyle from '@/components/Main/SafetyArtifactTree/GraphStyle'
import CytoscapePrototypeSAFA from '@/lib/cytoscape/prototypes/safa'
import LayoutTemplateKlay from '@/lib/cytoscape/layouts/layout-template-klay'

const L = LayoutTemplateKlay

export default {
  name: 'SafetyArtifactTree',
  props: {
    update: Number,
    resize: Number,
    treeId: String,
    isFetchingFromServer: Boolean
  },
  mixins: [CytoscapeMixin],

  computed: {
    ...mapGetters('projects.module', ['getHazardTree', 'getSafetyArtifactTree']),
    treeElements () {
      if (this.treeId) {
        return JSON.parse(JSON.stringify(this.getSafetyArtifactTree))
      }
      return JSON.parse(JSON.stringify(this.getHazardTree))
    },
    showSpinner () {
      return this.isFetchingFromServer || this.isUpdating
    }
  },

  watch: {
    resize () {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.cy.resize()
      }
    },
    update () {
      this.renderTree(this.$refs.cy)
    },
    treeId () {
      this.renderTree(this.$refs.cy)
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
    this.renderTree(this.$refs.cy)
  },

  methods: {
    ...mapActions('projects.module', ['fetchSafetyArtifactTree', 'fetchDeltaTrees']),
    ...mapActions('app.module', ['setSelectedArtifact']),

    async renderTree (container) {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.destroy()
        this.setSelectedArtifact({})
      }
      try {
        this.isUpdating = true
        await this.fetchSafetyArtifactTree({treeId: this.treeId, rootType: config.safa_tree.root_node_type})

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

        const component = this
        this.cytoscapeProto = new CytoscapePrototypeSAFA(container, this.treeElements, GraphOptions, GraphStyle, layout)
        await this.cytoscapeProto.run()
        this.cytoscapeProto.cy.on('select', 'node', evt => {
          component.$emit('select:node')
          component.setSelectedArtifact(evt.target.data())
        })
        this.cytoscapeProto.cy.on('click', () => this.setSelectedArtifact({}))
      } catch (e) {
        console.log(e)
        // TODO(Adam): Handle Error
      }
      this.isUpdating = false
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
