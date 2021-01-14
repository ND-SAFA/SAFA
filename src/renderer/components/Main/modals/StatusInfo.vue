<template>
  <div v-if="!isHidden">
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal modal-wrapper">
          <div class="modal-dialog modal-dialog-centered modal-md">
            <div class="modal-content">
              <div class="modal-header">
                <h5 v-if="modalResult.success === true" class="modal-title delta-modal-title" id="exampleModalCenterTitle">Success!</h5>
                <h5 v-else class="modal-title delta-modal-title" id="exampleModalCenterTitle">Something went wrong.</h5>
                <button type="button" class="close" aria-label="Close" @click="$emit('close')">
                  &times;
                </button>
              </div>
              <form v-if="modalResult.success === true" class="delta-form">
                <div class="modal-body">
                  <div class="form-group">
                    <label for="inputGroupSelect01" class="sml">
                      {{modalResult.message}}
                    </label>
                  </div>
                </div>
                <div class="modal-footer custom-modal-footer">
                  <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
                  <button v-if="modalResult.upload === true" download="fileName" href="fileData" type="button" class="btn btn-primary delta-save-button" @click="downloadFile()">Download Error Log</button>
                </div>
              </form>
              <form v-else class="delta-form">
                <div class="modal-body">
                  <div class="form-group">
                    <label for="inputGroupSelect01" class="sml" v-if="modalResult.success === false">
                        Error: {{modalResult.message}} For more info, please visit our <a @click="getHelp()" class="help-link">Help Page</a>. 
                    </label>
                  </div>
                </div>
                <div class="modal-footer custom-modal-footer">
                  <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
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

    data: {
      fileName: 'SAFAErrorLog.txt',
      fileData: 'SGVsbG9AV29ybGQ='
    },

    methods: {
      getHelp () {
        shell.openExternal('https://github.com/SAREC-Lab/SAFA-Documentation')
      },
      downloadFile () {
        console.log('will download file here')
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
