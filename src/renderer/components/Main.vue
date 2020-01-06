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
  import HeaderNav from './Main/HeaderNav'
  import LeftPanel from './Main/LeftPanel'
  import RightPanel from './Main/RightPanel'
  import SafetyArtifactTree from './Main/SafetyArtifactTree'
  import FaultTreeAnalysis from './Main/FaultTreeAnalysis'
  import ConfigureDeltaModal from './Main/modals/ConfigureDelta'

  export default {
    name: 'main-page',
    data: function () {
      return {
        rightPanel: {
          isHidden: true
        }
      }
    },
    components: { HeaderNav, LeftPanel, RightPanel, SafetyArtifactTree, FaultTreeAnalysis, ConfigureDeltaModal },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
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
