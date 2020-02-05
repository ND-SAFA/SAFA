<template>
  <div id="left-list-view" class="p-0 bg-light">
    <div class="d-flex flex-column pt-0 px-2 bg-wash mb-0">
      <div class="custom-control custom-switch py-1">
        <input v-model="deltaEnabled" @change="toggleDelta" type="checkbox" class="custom-control-input" id="delta-mode-switch">
        <label class="custom-control-label d-flex justify-content-between font-weight-bold text-uppercase" for="delta-mode-switch">Delta View Mode<span><i class="fas fa-play fa-rotate-270"></i></span></label>
      </div>
      <button type="button" class="btn btn-outline-secondary btn-sm btn-block" @click="showDeltaModal">
        Configure Delta
      </button>
    </div>

    <ul id="top-tabs" role="tablist" class="nav nav-tabs nav-fill pt-3 mb-3 bg-wash">
      <li class="nav-item">
        <a class="nav-link active" id="artifact-tree-tab" data-toggle="tab" href="#center-panel" role="tab" aria-controls="center-panel" aria-selected="true">Artifacts</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="fault-tree-tab" data-toggle="tab" href="#center-panel-2" role="tab" aria-controls="center-panel-2" aria-selected="false">Safety Model</a>
      </li>
    </ul>

    <HazardList />

    <div id="fta-list-panel" role="tabpanel" aria-labelledby="fault-tree-tab" class="d-none">
      <p class="font-weight-bold text-uppercase mb-2 px-2 d-flex justify-content-between align-items-center">
        Fault Trees
      </p>

      <div class="row px-2">
        <div class="col-sm-12">
          <div class="form-group has-search mb-1">
            <i class="fa fa-search form-control-feedback"></i>
            <label class="w-100">
              <input type="text" class="fta-search-bar form-control rounded-pill" placeholder="Search">
            </label>
          </div>
        </div>
      </div>

      <div class="scroll-nav">
        <ul id="fta-list" class="nav"></ul>
      </div>

    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import HazardList from '@/components/Main/LeftPanel/HazardList'

export default {
  name: 'LeftPanel',

  data () {
    return {
      deltaEnabled: false
    }
  },

  components: { HazardList },

  mounted () {
    this.deltaEnabled = this.getDeltaState.enabled
  },

  computed: {
    ...mapGetters('app.module', ['getDeltaState']),
    deltaState () {
      return JSON.parse(JSON.stringify(this.getDeltaState))
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
