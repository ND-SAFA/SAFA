<template>
  <div id="upload-modal" v-if="!isHidden">
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal modal-wrapper">
          <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 v-if="modalResult.success === true && this.allFilesPresent === true" class="modal-title delta-modal-title" id="exampleModalCenterTitle">Success!</h5>
                <h5 v-else-if="modalResult.success === true && this.allFilesPresent === false" class="modal-title delta-modal-title" id="exampleModalCenterTitle">Please Add More Files</h5>
                <h5 v-else class="modal-title delta-modal-title" id="exampleModalCenterTitle">Something went wrong.</h5>
                <button type="button" class="close" aria-label="Close" @click="$emit('close')">
                  &times;
                </button>
              </div>
              <span v-if="modalResult.success === true && this.allFilesPresent === false">
                  <div class="files-needed-caption sml">
                    More files are needed to accurately match system described in the TIM. If files are missing, please upload the correct files. If trace links need generating, click 'Project' -> 'Generate Trace 
                    Links' and approve links. Or, upload a new TIM to change the configuration. 
                  </div>
                <table class="table table-bordered table-sm upload-table">
                  <thead class="thead-light">
                    <tr>
                      <th scope="col">FileName</th>
                      <th scope="col">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in fileMap" :key="item.name" v-bind:class="{'table-danger bold-missing-files': item.status === 'Missing', 'table-warning bold-missing-files': item.status === 'Needs to be Generated'}">
                      <td scope="row">{{item.name}}</td> 
                      <td>{{item.status}}</td>
                    </tr>
                  </tbody>
                </table>
              </span>
              <form v-if="modalResult.success === true && this.allFilesPresent === true" class="delta-form">
                <div class="modal-body">
                  <div class="form-group">
                    <label for="inputGroupSelect01" class="sml">
                      Flatfiles were uploaded successfully. Do you want to synchronize data now?
                    </label>
                  </div>
                </div>
                <div class="modal-footer custom-modal-footer">
                  <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
                  <button type="submit" class="btn btn-primary delta-save-button" @click="$emit('sync-data')">Synchronize Data</button>
                </div>
              </form>
              <form v-else class="delta-form">
                <div class="modal-body">
                  <div class="form-group">
                    <label for="inputGroupSelect01" class="sml" v-if="modalResult.success === false">
                        Error: {{modalResult.message}}. For more info, please visit our <a @click="getHelp()" class="help-link">Help Page</a>. 
                    </label>
                  </div>
                </div>
                <div class="modal-footer custom-modal-footer">
                  <button v-if="modalResult.success === true && this.allFilesPresent === false" type="submit" class="btn btn-primary delta-save-button" @click="$emit('select-files')">Upload Files</button>
                  <button v-if="modalResult.success === true && this.allFilesPresent === false" type="submit" class="btn btn-primary delta-save-button" @click="$emit('generate-links')">Generate Links</button>
                  <button v-if="modalResult.success === true && this.allFilesPresent === false" type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
                  <button v-else type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
  import { shell } from 'electron'
  export default {
    props: {
      isHidden: Boolean,
      modalResult: Object
    },

    data () {
      return {
        allFilesPresent: false,
        fileMap: {}
      }
    },

    watch: {
      isHidden: function (newVal, oldVal) {
        console.log('running watcher')
        console.log(newVal)
        if (newVal === false) {
          this.compareFileLists()
        }
      }
    },

    methods: {
      compareFileLists () {
        if (this.modalResult.data) {
          this.fileMap = {}
          this.findMissingFiles(this.modalResult.data.uploadedFiles, this.modalResult.data.expectedFiles, false)
          this.findMissingFiles(this.modalResult.data.generatedFiles, this.modalResult.data.expectedGeneratedFiles, true)
          console.log('FILE MAP:')
          console.log(this.fileMap)
          this.allFilesPresent = true
          for (var key in this.fileMap) {
            if (this.fileMap[key].status === 'Missing' || this.fileMap[key].status === 'Needs to be Generated') this.allFilesPresent = false
          }
        }
      },

      findMissingFiles (foundFiles, expectedFiles, traceLinks) {
        console.log('found files: ', foundFiles)
        console.log('expected files: ', expectedFiles)
        for (var i = 0; i < expectedFiles.length; i++) {
          var entry = {}
          entry.name = expectedFiles[i]
          if (!traceLinks) {
            entry.status = 'Missing'
          } else {
            entry.status = 'Needs to be Generated'
          }
          this.fileMap[expectedFiles[i]] = entry
        }

        for (var j = 0; j < expectedFiles.length; j++) {
          for (var k = 0; k < foundFiles.length; k++) {
            if (foundFiles[k].toLowerCase() === expectedFiles[j].toLowerCase()) {
              var myEntry = this.fileMap[expectedFiles[j]]
              myEntry.status = 'Ready'
              this.fileMap[expectedFiles[j]] = myEntry
            }
          }
        }
      },

      getHelp () {
        shell.openExternal('https://github.com/SAREC-Lab/SAFA-Documentation')
      }
    }

  }
</script>

<style scoped>
  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: table;
    transition: opacity .3s ease;
  }

  .modal-wrapper {
    display: table-cell;
    vertical-align: middle;
  }

  .bold-missing-files {
    font-weight: bold;
  }

  .upload-table {
    margin: 2% 5% 1%; 
    width: 90%; 
    font-size: 14px; 
  }

  .files-needed-caption {
    padding: 1rem; 
  }

  .help-link {
    text-decoration: underline;
    color: blue; 
  }
  .help-link:hover {
    text-decoration: underline;
    color: blue; 
    cursor: pointer;
  }
</style>
