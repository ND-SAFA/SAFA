<template>
  <div id="center-panel" role="tabpanel" aria-labelledby="artifact-tree-tab" class="fade col show active graph-view p-0">
    <!-- <div id="loading-graph-spinner" v-show="showSpinner">
      <div class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div> -->
    <div id="center-panel-container">
      <div id="source-container"><span id="source-name">UAV-1800</span><span id="source-description">This artifact description will be moderately long, not too long though since we're still figuring things out. It will be kind of long though, so that it's definitely at least 2 or more lines and just goes on for awhile. It could go on for even a bit longer tbh because we know its gonna be long. </span></div>
      <hr/>
      <div id="target-info"><b>UAV-200:</b> This artifact description will be moderately long, not too long though since we're still figuring things out. It will be kind of long though, so that it's definitely at least 2 or more lines and just goes on for awhile. It could go on for even a bit longer tbh because we know its gonna be long </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 60%; height: 20px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio" checked>Not Vetted</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Approved</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Rejected</label>
            </div>
        </form>
      </div>
      <div id="target-info"><b>UAV-500:</b> This artifact description will be moderately long, not too long though since we're still figuring things out. It will be kind of long though, so that it's definitely at least 2 or more lines and just goes on for awhile. It could go on for even a bit longer tbh because we know its gonna be long </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 40%; height: 20px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio" checked>Not Vetted</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Approved</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Rejected</label>
            </div>
        </form>
      </div>
      <div id="target-info"><b>UAV-1200:</b> This artifact description will be moderately long, not too long though since we're still figuring things out. It will be kind of long though, so that it's definitely at least 2 or more lines and just goes on for awhile. It could go on for even a bit longer tbh because we know its gonna be long. This one can even be a bit longer because the div size will adjust to how long the text is. </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 30%; height: 20px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio" checked>Not Vetted</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Approved</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Rejected</label>
            </div>
        </form>
      </div>
      <div id="target-info"><b>UAV-1400:</b> This artifact description will be moderately long, not too long though since we're still figuring things out. It will be kind of long though, so that it's definitely at least 2 or more lines and just goes on for awhile. It could go on for even a bit longer tbh because we know its gonna be long. This one can even be a bit longer because the div size will adjust to how long the text is. </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 10%; height: 20px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio" checked>Not Vetted</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Approved</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Rejected</label>
            </div>
        </form>
      </div>
      <div id="target-info"><b>UAV-1400:</b> This artifact description will be moderately long, not too long though since we're still figuring things out. It will be kind of long though, so that it's definitely at least 2 or more lines and just goes on for awhile. It could go on for even a bit longer tbh because we know its gonna be long. This one can even be a bit longer because the div size will adjust to how long the text is. </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 10%; height: 20px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio" checked>Not Vetted</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Approved</label>
            </div>
            <div class="radio">
              <label><input type="radio" id="radio-input" name="optradio">Rejected</label>
            </div>
        </form>
      </div>     
          <div id="footer">
        <button type="button" class="btn btn-outline-primary">Primary</button>
        <button type="button" class="btn btn-outline-secondary">Secondary</button>
        <button type="button" class="btn btn-outline-success">Success</button>
    </div>   
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'ApproveLinks',

  computed: {
    ...mapGetters('projects.module', ['getHazardTree', 'getSafetyArtifactTree'])
  },

  methods: {
    ...mapActions('projects.module', ['fetchSafetyArtifactTree', 'fetchDeltaTrees']),
    ...mapActions('app.module', ['setSelectedArtifact'])
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
  #center-panel-container {
    line-height: 1.8; 
    margin: 20px 20px 0px; 
    max-height: calc(100vh - 140px);
    overflow: auto; 
  }
  #source-container {
    background-color: white;
    border-width: 1px; 
    border-style: solid;
    border-color: #c2c2c2;
    padding: 10px; 
    margin-bottom: 30px; 
    border-radius: 10px;
    font-size: 18px; 
  }
  #source-name {
    border-width: 2px; 
    border-style: solid; 
    padding: 3px; 
    margin-right: 10px; 
    font-weight: bold; 
    font-size: 20px; 
  }
  #target-info {
    width: 75%; 
    float: left;
    margin: 15px 0px 15px; 
    max-height: 130px; 
    text-overflow: ellipsis; 
    display: block;
    overflow: hidden; 
    background-color: white;
    border-width: 1px; 
    border-style: solid;
    border-color: #c2c2c2;
    padding: 10px; 
    padding-right: 20px; 
    border-radius: 10px;
    font-size: 16px; 
  }
  #target-right-info {
    width: 25%; 
    float: left; 
    line-height: 1.2; 
    margin: 15px 0px 15px; 
  }
  #progress-bar {
    background-color: #919191;
    width: 60%; 
    margin: auto; 
    height: 20px; 
  }
  #radio-buttons {
    margin: auto; 
    width: 60%; 
    margin-top: 15px; 
    margin-left: 25%; 
  }
  #radio-input {
    margin-right: 5px; 
  }
  #footer {
   position:fixed;
   right:0px;
   bottom:0px;
   height:80px;
   width:100%;
   margin: auto; 
   float: right; 
  }
</style>
