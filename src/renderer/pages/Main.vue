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
              <LeftPanel v-on:show-delta-modal="showDeltaModal = true"/>
              <DeltaTree v-if="getDeltaState.enabled && getSelectedTree" v-bind:tree-id="getSelectedTree" />
              <SafetyArtifactTree v-else v-bind:tree-id="getSelectedTree"/>
              <FaultTree />
              <RightPanel v-bind:is-hidden="rightPanel.isHidden" v-on:open:link="open"/>
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
  import FaultTree from '@/components/Main/FaultTree'
  import DeltaTree from '@/components/Main/DeltaTree'
  import ConfigureDeltaModal from '@/components/Main/modals/ConfigureDelta'

  export default {
    name: 'main-page',
    components: { HeaderNav, LeftPanel, RightPanel, SafetyArtifactTree, FaultTree, DeltaTree, ConfigureDeltaModal },

    data: function () {
      return {
        showDeltaModal: false,
        isFetchingFromServer: false,
        rightPanel: {
          isHidden: true
        }
      }
    },
    computed: {
      ...mapGetters('projects.module', ['getHazards']),
      ...mapGetters('app.module', ['getDeltaState', 'getSelectedTree'])
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
