<template>
  <div id="mainpage">

    <!-- Header Nav -->
    <HeaderNav v-bind:right-panel="rightPanel" />

    <div class="d-flex" id="wrapper">

      <!-- Page Content -->
      <div id="page-content-wrapper">
        <main role="main">
          <div class="container-fluid">
            <div class="row vh-100 pad-navbar">
              <LeftPanel v-bind:left-panel="leftPanel" v-on:show-delta-modal="showDeltaModal = true"/>
              <SafetyArtifactTree v-bind:tree-id="leftPanel.selectedTreeId" v-on:unselect-node="unselectNode"/>
              <FaultTreeAnalysis/>
              <RightPanel v-bind:is-hidden="rightPanel.isHidden"/>
            </div>
            <ConfigureDeltaModal v-bind:is-hidden="!showDeltaModal" @close="showDeltaModal = false" />
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
  import FaultTreeAnalysis from '@/components/Main/FaultTreeAnalysis'
  import ConfigureDeltaModal from '@/components/Main/modals/ConfigureDelta'

  export default {
    name: 'main-page',
    components: { HeaderNav, LeftPanel, RightPanel, SafetyArtifactTree, FaultTreeAnalysis, ConfigureDeltaModal },

    data: function () {
      return {
        showDeltaModal: false,
        isFetchingFromServer: false,
        rightPanel: {
          isHidden: true,
          selectedNode: null
        },
        leftPanel: {
          selectedTreeId: null
        }
      }
    },
    computed: {
      ...mapGetters('projects.module', ['getHazards'])
    },
    created () {
      AppMenu.findMenuItemById('view.refresh').click = this.reloadData.bind(this)
      AppMenu.setApplicationMenu()
    },
    methods: {
      ...mapActions('projects.module', ['fetchHazards', 'fetchHazardTree']),
      open (link) {
        this.$electron.shell.openExternal(link)
      },
      unselectNode (evt, target, selector) {
        console.log(evt, target, selector)
      },
      reloadData () {
        console.log('reloadData()')
      }
    },
    async mounted () {
      this.isFetchingFromServer = true
      await this.fetchHazards()
      await this.fetchHazardTree()
      this.isFetchingFromServer = false
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
  @import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css';
  @import '../../../node_modules/@fortawesome/fontawesome-free/css/all.min.css';
  @import '../styles/safa.css';
</style>
