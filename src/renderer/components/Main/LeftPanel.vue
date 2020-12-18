<template>
  <div id="left-list-view" class="p-0 bg-light">
    <div class="d-flex flex-column pt-0 px-2 bg-wash mb-0">
      <div class="custom-control custom-switch py-1 mb-10">
        <input v-model="deltaEnabled" @change="toggleDelta" type="checkbox" class="custom-control-input" id="delta-mode-switch">
        <label class="custom-control-label d-flex justify-content-between font-weight-bold text-uppercase" for="delta-mode-switch">Delta View Mode<span><i class="fas fa-play fa-rotate-270"></i></span></label>
      </div>
      <button type="button" class="btn btn-outline-secondary btn-sm btn-block" @click="showDeltaModal">
        Configure Delta
      </button>
    </div>

    <div class="d-flex flex-column pt-0 px-2 bg-wash mb-0">
      <div style="padding-top: 10px; ">
        <p class="font-weight-bold text-uppercase mb-2 d-flex justify-content-between align-items-center">
          Manage Data
        </p>
        <input type="file" id="selectedFile" style="display: none;" @change="uploadFiles"/>
        <input type="button" class="btn btn-outline-secondary btn-sm btn-block" value="Upload Flatfiles" onclick="document.getElementById('selectedFile').click();" />
      </div>
    </div>

    <ul id="top-tabs" role="tablist" class="nav nav-tabs nav-fill pt-3 mb-3 bg-wash">
      <li class="nav-item">
        <a @click="toggleArtifactsTab" class="nav-link active" id="artifact-tree-tab" data-toggle="tab" href="#center-panel" role="tab" aria-controls="center-panel" aria-selected="true">Artifacts</a>
      </li>
      <li class="nav-item">
        <a @click="toggleFTATab" class="nav-link" id="fault-tree-tab" data-toggle="tab" href="#center-panel-2" role="tab" aria-controls="center-panel-2" aria-selected="false">Safety Model</a>
      </li>
    </ul>

    <HazardList v-if="showTab === 'Artifacts'" />

    <FTANodeList v-if="showTab === 'FTA'" />

  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import HazardList from '@/components/Main/LeftPanel/HazardList'
import FTANodeList from '@/components/Main/LeftPanel/FTANodeList'

export default {
  name: 'LeftPanel',

  data () {
    return {
      deltaEnabled: false,
      showTab: 'Artifacts'
    }
  },

  components: { HazardList, FTANodeList },

  mounted () {
    this.deltaEnabled = this.getDeltaState.enabled
  },

  computed: {
    ...mapGetters('app.module', ['getDeltaState']),

    deltaState () {
      return JSON.parse(JSON.stringify(this.getDeltaState))
    },

    isProjectInitialized () {
      return !(this.getDeltaState.current === -1)
    }
  },

  watch: {
    'deltaState.enabled' () {
      this.deltaEnabled = this.deltaState.enabled
    }
  },

  methods: {
    ...mapActions('app.module', ['updateDelta']),
    showDeltaModal () {
      this.$emit('show-delta-modal')
    },

    toggleDelta () {
      const deltaState = this.deltaState
      deltaState.enabled = this.deltaEnabled
      this.updateDelta(deltaState)
    },

    toggleArtifactsTab () {
      this.showTab = 'Artifacts'
    },

    toggleFTATab () {
      this.showTab = 'FTA'
    },

    uploadFiles (e) {
      console.log('uploading files bb')
      console.log(e.target.files[0])
    }
  }
}
</script>

<style scoped>
.custom-switch label {
  font-size: 0.9rem;
  padding-top: 0.1rem;
}
</style>
