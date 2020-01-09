<template>
  <div id="mainpage">
    
    <!-- Header Nav -->
    <HeaderNav v-bind:right-panel="rightPanel"/>

    <div class="d-flex" id="wrapper">

      <!-- Page Content -->
      <div id="page-content-wrapper">
        <main role="main">
          <div class="container-fluid">
            <div class="row vh-100 pad-navbar">
              <LeftPanel/>
              <SafetyArtifactTree/>
              <FaultTreeAnalysis/>
              <RightPanel v-bind:is-hidden="rightPanel.isHidden"/>
            </div> 
            <ConfigureDeltaModal/>
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
          isHidden: true
        },
        leftPanel: {
        }
      }
    },
    computed: {
      ...mapGetters('projects.module', ['getHazards'])
    },
    methods: {
      ...mapActions('projects.module', ['fetchHazards']),
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    },
    async mounted () {
      if (this.getHazards.length === 0) {
        this.isFetchingFromServer = true
        await this.fetchHazards()
        this.isFetchingFromServer = false
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
