<template>
  <div v-if="!isHidden">
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
                    More files are needed to accurately match system described in the TIM. Please upload missing files or upload a new TIM. 
                  </div>
                <table class="table table-bordered table-sm upload-table">
                  <thead>
                    <tr>
                      <th scope="col">FileName</th>
                      <th scope="col">Present</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in fileMap" :key="item.name" v-bind:class="{ 'table-danger bold-missing-files': item.found == false }" >
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
                  <button id="sync" type="submit" class="btn btn-primary delta-save-button">Synchronize Data</button>
                </div>
              </form>
              <form v-else class="delta-form">
                <div class="modal-body">
                  <div class="form-group">
                    <label for="inputGroupSelect01" class="sml" v-if="modalResult.success === false">
                        Could not upload flatfiles. Please try again.
                    </label>
                  </div>
                </div>
                <div class="modal-footer custom-modal-footer">
                  <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
                  <button v-if="modalResult.success === true && this.allFilesPresent === false" type="submit" class="btn btn-primary delta-save-button">Add Additional Files</button>
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

export default {
  props: {
    isHidden: Boolean,
    modalResult: Object
  },

  data () {
    return {
      allFilesPresent: false,
      fileMap: [],
      items: [
        {age: 30, first_name: 'Emma', last_name: 'Watson'},
        {age: 31, first_name: 'Daniel', last_name: 'Radcliff'}
      ]
    }
  },

  watch: {
    'isHidden' () {
      this.compareFileLists()
    }
  },

  methods: {
    compareFileLists () {
      var allFiles = this.modalResult.message.allFiles
      var currentFiles = this.modalResult.message.currentFiles
      var missingFiles = false
      var entry = {}

      for (var i = 0; i < allFiles.length; i++) {
        var found = false
        for (var j = 0; j < currentFiles.length; j++) {
          if (allFiles[i] === currentFiles[j]) {
            entry = {}
            entry.name = allFiles[i]
            entry.status = 'Present'
            entry.found = true
            found = true
            this.fileMap.push(entry)
          }
        }

        if (!found) {
          entry = {}
          entry.name = allFiles[i]
          entry.status = 'Missing'
          entry.found = false
          missingFiles = true
          this.fileMap.push(entry)
        }
      }

      if (!missingFiles) {
        this.allFilesPresent = true
      } else {
        this.allFilesPresent = false
      }

      console.log(this.allFilesPresent)
      console.log(this.fileMap)
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
</style>
