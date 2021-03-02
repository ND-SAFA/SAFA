<template>
<div>
  <div v-if="!approvalView && !timView" id="mainpage">
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
                      v-on:refresh:view="refreshView" 
                      v-on:show-upload-modal="triggerUploadModal"/>
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
              <FaultTree :resize="resize" v-on:select:node="openRightPanel"/>
              <RightPanel v-show="!rightPanel.isHidden" v-on:open:link="open"/>
            </div>
            <ConfigureDeltaModal :is-hidden="!showDeltaModal" @close="showDeltaModal = false" />
            <FileUploadResultsModal :is-hidden="!showUploadModal" :modal-result="uploadResult" @close="showUploadModal = false" @select-files="uploadMoreFiles" @generate-links="projectGenerate" @sync-data="projectSync"/>
            <StatusInfoModal :is-hidden="!showInfoModal" @close="showInfoModal = false" :modal-result="showInfoResult" :type="uploadModalType" @approve-links="switchToApprovalView"/>
          </div>
        </main>
      </div>
      <!-- End Page Content -->

    </div>
  </div>
  <div v-if="approvalView === true" id="mainpage">
    <HeaderNav :right-panel="rightPanel" :left-panel="leftPanel" v-on:resize:view="resizeView"/>
    <div class="d-flex" id="wrapper">
      <div id="page-content-wrapper">
        <main role="main">
          <div class="container-fluid">
            <div class="row vh-100 pad-navbar">
              <LinksLeftPanel :type-data="linkTypeData" @artifact-data="choseArtifactData" @chosen-artifact="selectArtifactIndex"/>
              <ApproveLinks :artifact-data="chosenArtifactData" :artifact-index="chosenArtifactIndex" @close-approver="approvalView = false"/>
            </div>
          </div>
        </main>
      </div>
      <!-- End Page Content -->

    </div>
  </div>
  <div v-if="timView === true" id="mainpage">
    <HeaderNav :right-panel="rightPanel" :left-panel="leftPanel" v-on:resize:view="resizeView"/>
    <div class="d-flex" id="wrapper">
      <div id="page-content-wrapper">
        <main role="main">
          <div class="container-fluid">
            <div class="row vh-100 pad-navbar">
              <TimGraph @undo-tim="switchOffTIMView"/>
            </div>
          </div>
        </main>
      </div>
      <!-- End Page Content -->

    </div>
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
  import LinksLeftPanel from '@/components/Main/LinksLeftPanel'
  import ApproveLinks from '@/components/Main/ApproveLinks'
  import ConfigureDeltaModal from '@/components/Main/modals/ConfigureDelta'
  import FileUploadResultsModal from '@/components/Main/modals/FileUploadResults'
  import StatusInfoModal from '@/components/Main/modals/StatusInfo'
  import TimGraph from '@/components/Main/TimGraph'

  export default {
    name: 'main-page',
    components: {
      HeaderNav,
      LeftPanel,
      RightPanel,
      SafetyArtifactTree,
      FaultTree,
      DeltaTree,
      LinksLeftPanel,
      ApproveLinks,
      ConfigureDeltaModal,
      FileUploadResultsModal,
      StatusInfoModal,
      TimGraph
    },

    data () {
      return {
        firstOpen: true,
        approvalView: false,
        timView: false,
        resize: Date.now(),
        update: Date.now(),
        showDeltaModal: false,
        showUploadModal: false,
        uploadModalType: '',
        linkTypeData: null,
        chosenArtifactData: {},
        chosenArtifactIndex: 0,
        uploadResult: null,
        showInfoModal: false,
        showInfoResult: null,
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
      AppMenu.findMenuItemById('project.sync').click = this.projectSync.bind(this)
      AppMenu.findMenuItemById('project.upload').click = this.projectUpload.bind(this)
      AppMenu.findMenuItemById('project.clear').click = this.clearFiles.bind(this)
      AppMenu.findMenuItemById('project.generate').click = this.projectGenerate.bind(this)
      AppMenu.findMenuItemById('project.approve').click = this.switchToApprovalView.bind(this)
      AppMenu.findMenuItemById('project.tim').click = this.switchToTIMView.bind(this)
      AppMenu.findMenuItemById('project.remove').click = this.projectRemove.bind(this)
      AppMenu.setApplicationMenu()
    },

    async mounted () {
      // this.resetApp()
      // this.resetProject()
      this.loadData()
    },

    methods: {
      ...mapActions('projects.module', ['syncProject', 'fetchHazards', 'fetchHazardTree', 'fetchSafetyArtifactTree', 'fetchProjectVersions', 'resetProject', 'uploadFlatfileData',
        'fetchErrorLog', 'generateTraceLinks', 'getGeneratedLinks', 'getGenerateLinksErrorLog', 'removeTraceLinks', 'clearUploads', 'getLinkTypes']),
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
        if (this.firstOpen) {
          this.firstOpen = false
          this.updateView()
        }
      },
      async projectSync () {
        this.showUploadModal = false
        var response = {}
        try {
          await this.syncProject().then((syncResponse) => {
            if (syncResponse.file) {
              response.data = syncResponse.file
              response.success = true
              response.message = 'Missing the following files from upload: '
              this.triggerUploadModal(response)
            } else if (syncResponse.message) {
              response.success = false
              response.message = syncResponse.message
              this.triggerInfoModal(response, 'upload')
            } else {
              this.fetchErrorLog().then((encodedLog) => { // only do if successful
                response.success = true
                response.message = 'Data Upload Successful.'
                response.data = encodedLog
                this.triggerInfoModal(response, 'upload')
              })
            }
          })
        } catch (e) {
          response.success = false
          response.message = e
          this.triggerInfoModal(response, 'upload')
        }
      },
      async switchToApprovalView () {
        await this.getLinkTypes().then(result => {
          this.linkTypeData = result
        })
        this.showInfoModal = false
        this.approvalView = true
        this.timView = false
        this.enableOptions(false)
      },
      switchToTIMView () {
        this.showInfoModal = false
        this.timView = true
        this.approvalView = false
        this.enableOptions(false)
      },
      switchOffTIMView () {
        this.showInfoModal = false
        this.timView = false
        this.approvalView = false
        this.enableOptions(true)
      },
      resizeView () {
        this.resize = Date.now()
      },
      updateView () {
        this.update = Date.now()
      },
      openRightPanel () {
        this.rightPanel.isHidden = false
      },
      triggerUploadModal (uploadResponse) {
        this.uploadResult = uploadResponse
        this.showUploadModal = true
      },
      readFiles (filename) {
        return new Promise((resolve, reject) => {
          var fs = require('fs')
          fs.readFile(filename, {encoding: 'base64'}, (err, data) => {
            if (err) {
              reject(err)
            }
            resolve(data)
          })
        })
      },
      async uploadFiles (files) {
        let results = await Promise.all(
          files.map(async file => {
            let myData = await this.readFiles(file)
            var pieces = file.split('/')
            return [pieces[pieces.length - 1], myData]
          })
        )
        var dict = {}
        for (var result of results) {
          dict[result[0]] = result[1]
        }
        return dict
      },
      async projectUpload () {
        const { dialog } = require('electron').remote
        const chosenFolders = await dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] })
        this.uploadFiles(chosenFolders).then(result => {
          console.log(result)
          this.uploadFlatfileData(JSON.stringify(result)).then(response => { this.triggerUploadModal(response) })
        })
      },
      async uploadMoreFiles () {
        this.showUploadModal = false
        this.$nextTick(() => { this.projectUpload() })
      },
      triggerInfoModal (response, type) {
        this.uploadModalType = type
        if (type === 'upload' || type === 'generate') {
          response.errorLog = true
        } else {
          response.errorLog = false
        }
        response.type = type
        this.showInfoResult = response
        this.showInfoModal = true
      },
      async projectGenerate () {
        this.showUploadModal = false
        await this.generateTraceLinks().then(response => {
          console.log(response.message)
          if (response.success) {
            this.getGenerateLinksErrorLog().then(errorresult => {
              response.data = errorresult
              this.triggerInfoModal(response, 'generate')
            })
          } else {
            this.triggerInfoModal(response, 'generate')
          }
        })
      },
      async projectRemove () {
        this.removeTraceLinks().then(result => { this.triggerInfoModal(result, 'remove') })
      },
      async clearFiles () {
        this.clearUploads().then(result => { this.triggerInfoModal(result, 'delete') })
      },
      selectArtifactIndex (index) {
        console.log('new artifact found in main? ', index)
        this.chosenArtifactIndex = index
      },
      choseArtifactData (linkdata) {
        this.chosenArtifactData = linkdata
      },
      enableOptions (status) {
        AppMenu.findMenuItemById('project.sync').enabled = status
        AppMenu.findMenuItemById('project.freeze').enabled = status
        AppMenu.findMenuItemById('project.upload').enabled = status
        AppMenu.findMenuItemById('project.clear').enabled = status
        AppMenu.findMenuItemById('project.generate').enabled = status
        AppMenu.findMenuItemById('project.approve').enabled = status
        AppMenu.findMenuItemById('project.remove').enabled = status
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
