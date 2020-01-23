<template>
  <div id="mainpage">

    <!-- Header Nav -->
    <HeaderNav v-bind:right-panel="rightPanel" v-bind:versions="leftPanel.versions" v-bind:show-versions="leftPanel.deltaMode"/>

    <div class="d-flex" id="wrapper">

      <!-- Page Content -->
      <div id="page-content-wrapper">
        <main role="main">
          <div class="container-fluid">
            <div class="row vh-100 pad-navbar">
              <LeftPanel v-bind:left-panel="leftPanel"/>
              <SafetyArtifactTree v-bind:tree-id="leftPanel.selectedTreeId" v-on:unselect-node="unselectNode"/>
              <FaultTreeAnalysis/>
              <RightPanel v-bind:is-hidden="rightPanel.isHidden"/>
            </div>
            <ConfigureDeltaModal v-bind:is-hidden="!leftPanel.showDeltaModal" v-bind:left-panel="leftPanel" @close="leftPanel.showDeltaModal = false"/>
          </div>
        </main>
      </div>
      <!-- End Page Content -->

    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
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
        isFetchingFromServer: false,
        rightPanel: {
          isHidden: true,
          selectedNode: null
        },
        leftPanel: {
          selectedTreeId: null,
          showDeltaModal: false,
          deltaMode: false,
          versions: {
            available: [ 1 ],
            current: 1,
            baseline: 1
          }
        }
      }
    },
    computed: {
      ...mapGetters('projects.module', ['getHazards'])
    },
    methods: {
      ...mapActions('projects.module', ['fetchHazards', 'fetchHazardTree']),
      open (link) {
        this.$electron.shell.openExternal(link)
      },
      unselectNode (evt, target, selector) {
        console.log(evt, target, selector)
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
