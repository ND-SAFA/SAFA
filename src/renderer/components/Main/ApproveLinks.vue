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
      <div id="source-container"><span id="source-name">UAV-1800</span><span id="source-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at</span></div>
      <hr/>
      <div id="target-info" @dblclick="expandDesc()"><b>UAV-1400:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at, ornare neque. Mauris in enim nibh. Nullam eu odio eget elit lacinia maximus. Nulla vitae magna dui. Fusce vel lectus scelerisque enim rutrum consequat at et ante. Morbi non  </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 20%; height: 10px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label" checked>Not Vetted</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Approved</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Rejected</label>
            </div>
        </form>
      </div>  
      <div id="target-info"><b>UAV-1400:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at, ornare neque. Mauris in enim nibh. Nullam eu odio eget elit lacinia maximus. Nulla vitae magna dui. Fusce vel lectus scelerisque enim rutrum consequat at et ante. Morbi non  </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 20%; height: 10px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label" checked>Not Vetted</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Approved</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Rejected</label>
            </div>
        </form>
      </div>  
      <div id="target-info"><b>UAV-1400:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at, ornare neque. Mauris in enim nibh. Nullam eu odio eget elit lacinia maximus. Nulla vitae magna dui. Fusce vel lectus scelerisque enim rutrum consequat at et ante. Morbi non  </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 20%; height: 10px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label" checked>Not Vetted</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Approved</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Rejected</label>
            </div>
        </form>
      </div>  
      <div id="target-info"><b>UAV-1400:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at, ornare neque. Mauris in enim nibh. Nullam eu odio eget elit lacinia maximus. Nulla vitae magna dui. Fusce vel lectus scelerisque enim rutrum consequat at et ante. Morbi non  </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 20%; height: 10px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label" checked>Not Vetted</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Approved</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Rejected</label>
            </div>
        </form>
      </div>  
      <div id="target-info"><b>UAV-1400:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at, ornare neque. Mauris in enim nibh. Nullam eu odio eget elit lacinia maximus. Nulla vitae magna dui. Fusce vel lectus scelerisque enim rutrum consequat at et ante. Morbi non  </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 20%; height: 10px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label" checked>Not Vetted</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Approved</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Rejected</label>
            </div>
        </form>
      </div>     
      <div id="target-info"><b>UAV-1400:</b> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nunc velit, lobortis ac leo vitae, lobortis rhoncus erat. Fusce sapien turpis, hendrerit eget tempus eget, egestas ut erat. Nullam odio purus, egestas sit amet pulvinar vitae, mollis et eros. Donec pretium fermentum luctus. Fusce a orci tristique, semper mauris at, ornare neque. Mauris in enim nibh. Nullam eu odio eget elit lacinia maximus. Nulla vitae magna dui. Fusce vel lectus scelerisque enim rutrum consequat at et ante. Morbi non  </div>
      <div id="target-right-info">
        <div id="progress-bar">
          <div class="progress-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: 20%; height: 10px"></div>
        </div>
        <form class="form" id="radio-buttons">
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label" checked>Not Vetted</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Approved</label>
            </div>
            <div>
              <label id="radio-input" ><input type="radio" name="optradio" id="radio-label">Rejected</label>
            </div>
        </form>
      </div>  
      <div id="footer">
        <div id="save-buttons">
            <button id="save-button" type="button" class="btn btn-outline-primary">Save All</button>
            <button id="save-button" type="button" class="btn btn-outline-primary">Save All and Exit</button>
            <button id="save-button" type="button" class="btn btn-outline-danger">Exit without Saving</button>
        </div>
      </div>   
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'ApproveLinks',

  computed: {
    ...mapGetters('projects.module', ['getHazardTree'])
  },

  methods: {
    ...mapActions('projects.module', ['fetchDeltaTrees']),
    ...mapActions('app.module', ['setSelectedArtifact']),
    testfunc () {
      console.log('test info')
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
  #center-panel-container {
    line-height: 1.6; 
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
    font-size: 15px; 
  }
  #source-name {
    border-width: 2px; 
    border-style: solid; 
    padding: 3px; 
    margin-right: 10px; 
    font-weight: bold; 
    font-size: 20px; 
    border-radius: 5px;
  }
  #target-info {
    width: 85%; 
    float: left;
    margin: 8px 0px 8px; 
    max-height: 68px; 
    text-overflow: ellipsis; 
    display: block;
    overflow: hidden; 
    background-color: white;
    border-width: 1px; 
    border-style: solid;
    border-color: #c2c2c2;
    padding: 5px; 
    padding-right: 20px; 
    border-radius: 10px;
    font-size: 13px; 
    line-height: 1.2; 
  }
  #target-right-info {
    width: 15%; 
    float: left; 
    margin: 5px 0px 5px; 
    font-size: 11px; 
  }
  #progress-bar {
    background-color: #adadad;
    width: 60%; 
    margin: auto; 
    height: 10px; 
  }
  #radio-buttons {
    width: 60%; 
    margin-top: 5px; 
    margin-left: 25%; 
  }
  #radio-input {
    margin-bottom: 2px; 
  }
  #radio-label {
    margin-right: 5px; 
  }
  #footer {
   position: fixed;
   bottom: 0px;
   height: 80px;
   width: 100%;
   margin: auto; 
  }
  #save-buttons {
    position: fixed;
    right: 20px; 
    padding-top: 20px;
  }
  #save-button {
    margin: 0px 5px 0px; 
  }
</style>
