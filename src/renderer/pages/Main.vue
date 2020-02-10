<template>
  <div id="mainpage">

    <!-- Header Nav -->
    <HeaderNav :right-panel="rightPanel" :left-panel="leftPanel" v-on:resize:view="resizeView"/>

    <div class="d-flex" id="wrapper">

      <!-- Page Content -->
      <div id="page-content-wrapper">
        <main role="main">
          <div class="container-fluid">
            <div class="row vh-100 pad-navbar">
              <LeftPanel v-show="!leftPanel.isHidden" 
                      v-on:show-delta-modal="showDeltaModal = true" 
                      v-on:refresh:view="refreshView" />
              <DeltaTree v-if="getDeltaState.enabled && getSelectedTree" 
                      :tree-id="getSelectedTree" 
                      :is-fetching-from-server="isFetchingFromServer" 
                      :resize="resize" 
                      :update="update"
                      v-on:select:node="openRightPanel"/>
              <SafetyArtifactTree v-else 
                      :tree-id="getSelectedTree" 
                      :is-fetching-from-server="isFetchingFromServer"
                      :resize="resize"
                      :update="update"
                      v-on:select:node="openRightPanel"/>
              <FaultTree />
              <RightPanel v-show="!rightPanel.isHidden" v-on:open:link="open"/>
            </div>
            <ConfigureDeltaModal :is-hidden="!showDeltaModal" @close="showDeltaModal = false" />
          </div>
        </main>
      </div>
      <!-- End Page Content -->

    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  import AppMenu from '@/menu'
  import HeaderNav from '@/components/Main/HeaderNav'
  import LeftPanel from '@/components/Main/LeftPanel'
  import RightPanel from '@/components/Main/RightPanel'
  import SafetyArtifactTree from '@/components/Main/SafetyArtifactTree'
  import FaultTree from '@/components/Main/FaultTree'
  import DeltaTree from '@/components/Main/DeltaTree'
  import ConfigureDeltaModal from '@/components/Main/modals/ConfigureDelta'

  export default {
    name: 'main-page',
    components: {
      HeaderNav,
      LeftPanel,
      RightPanel,
      SafetyArtifactTree,
      FaultTree,
      DeltaTree,
      ConfigureDeltaModal
    },

    data () {
      return {
        resize: Date.now(),
        update: Date.now(),
        showDeltaModal: false,
        isFetchingFromServer: false,
        rightPanel: {
          isHidden: true
        },
        leftPanel: {
          isHidden: false
        }
      }
    },

    computed: {
      ...mapGetters('projects.module', ['getHazards']),
      ...mapGetters('app.module', ['getDeltaState', 'getSelectedTree'])
    },

    created () {
      AppMenu.findMenuItemById('view.refresh').click = this.loadData.bind(this)
      AppMenu.setApplicationMenu()
    },

    async mounted () {
      // this.resetApp()
      // this.resetProject()
      this.loadData()
    },

    methods: {
      ...mapActions('projects.module', ['fetchHazards', 'fetchHazardTree', 'fetchSafetyArtifactTree', 'fetchProjectVersions']),
      ...mapActions('app.module', ['resetApp']),
      open (link) {
        this.$electron.shell.openExternal(link)
      },
      refreshView () {
        this.loadData()
        this.updateView()
      },
      async loadData () {
        this.isFetchingFromServer = true
        await this.fetchProjectVersions()
        await this.fetchHazards()
        if (this.getSelectedTree) {
          await this.fetchSafetyArtifactTree(this.getSelectedTree)
        } else {
          await this.fetchHazardTree()
        }
        this.isFetchingFromServer = false
      },
      resizeView () {
        this.resize = Date.now()
      },
      updateView () {
        this.update = Date.now()
      },
      openRightPanel () {
        console.log('called')
        this.rightPanel.isHidden = false
      }
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
  @import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css';
  @import '../../../node_modules/@fortawesome/fontawesome-free/css/all.min.css';
  @import '../styles/safa.css';
</style>
