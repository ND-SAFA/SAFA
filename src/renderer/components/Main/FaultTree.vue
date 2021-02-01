<template>
  <div id="center-panel-2" role="tabpanel" aria-labelledby="fault-tree-tab" aria-hidden="true" class="col d-none graph-view p-0">
    <div id="loading-graph-spinner" v-show="showSpinner">
      <div class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>
    <div id="cy-fta-error" class="alert alert-warning alert-dismissible fade show" role="alert" style="display:none">
      <span id="cy-fta-error-text">Problem Rendering the FTA.</span>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div v-if="elements.length==0" id="message">
        <p>Load a fault tree by selecting "File <i class="fas fa-arrow-right"></i> Open FTA File" from the application menu.</p>
    </div>
    <div id="cy-fta-parent">
      <div id="cy-fta" ref="cyfta"></div>
    </div>
  </div>
</template>

<script>
import fs from 'fs'
import Electron from 'electron'
// import { mapActions, mapGetters } from 'vuex'
import AppMenu from '@/menu'
import Vue from 'vue'
import CytoscapeMixin from '@/mixins/cytoscape-graph'
import * as GraphOptions from '@/components/Main/FaultTree/GraphOptions'
import GraphStyle from '@/components/Main/FaultTree/GraphStyle'
import CytoscapePrototypeFTA from '@/lib/cytoscape/prototypes/fta'
import LayoutTemplateKlay from '@/lib/cytoscape/layouts/layout-template-klay'

const { dialog } = Electron.remote
const L = LayoutTemplateKlay

export default {
  name: 'FaultTreeAnalysis',
  mixins: [CytoscapeMixin],
  props: {
    update: Number,
    resize: Number
  },

  data () {
    return {
      cytoscapeProto: Object(),
      isUpdating: false,
      elements: []
    }
  },

  computed: {
    showSpinner () {
      return this.isUpdating
    }
  },

  created () {
    AppMenu.findMenuItemById('file.open_fta').click = this.openFTAFile.bind(this)
    AppMenu.setApplicationMenu()
  },

  watch: {
    resize () {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.cy.resize()
      }
    },
    update () {
      this.renderTree(this.$refs.cyfta)
    }
  },

  mounted () {
    this.renderTree(this.$refs.cyfta)
  },

  methods: {
    async openFTAFile () {
      const readFile = new Promise((resolve, reject) => {
        dialog.showOpenDialog({ properties: ['openFile'] }, resolve)
      })
      const file = await readFile
      if (file) {
        this.isUpdating = true
        try {
          this.elements = JSON.parse(fs.readFileSync(file[0]))
          this.renderTree(this.$refs.cyfta)
          document.getElementById('fault-tree-tab').click()
        } catch (e) {
          // TODO(Adam): Handle could not parse JSON
        }
        this.isUpdating = false
      }
    },

    renderTree (container) {
      if (!Vue.isEmpty(this.cytoscapeProto)) {
        this.cytoscapeProto.destroy()
      }
      try {
        this.isUpdating = true
        const layout = new LayoutTemplateKlay({
          zoom: 1.1,
          spacing: 30,
          direction: L.DIRECTION.DOWN,
          fixedAlignment: L.FIXED_ALIGNMENT.BALANCED,
          layoutHierarchy: true,
          nodeLayering: L.NODE_LAYERING.NETWORK_SIMPLEX,
          nodePlacement: L.NODE_PLACEMENT.BRANDES_KOEPF,
          inLayerSpacingFactor: 1.0,
          thoroughness: 7
        })

        const component = this
        this.cytoscapeProto = new CytoscapePrototypeFTA(container, this.elements, GraphOptions, GraphStyle, layout)
        this.cytoscapeProto.run()
        this.cytoscapeProto.cy.on('select', 'node', evt => {
          component.$emit('select:node')
        })
        // this.cytoscapeProto.cy.on('click', () => )
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

  #message {
    padding-top: 25%;
  }

  #message p {
    font-size: 1.1rem;
    text-align: center;
  }

  #message i {
    font-size: .8rem;
  }
</style>