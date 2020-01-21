<template>
  <div v-if="!isHidden">
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal modal-wrapper">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title delta-modal-title" id="exampleModalCenterTitle">Configure Delta</h5>
                <button type="button" class="close" aria-label="Close" @click="$emit('close')">
                  &times;
                </button>
              </div>
              <form class="delta-form" @submit="enableDeltaMode">
                <div class="modal-body">
                  <div class="form-group">
                    <label for="inputGroupSelect01" class="sml">
                      Set current version:
                    </label>
                    <select v-model.number="versions.selectedCurrent" class="custom-select delta-current-select" id="inputGroupSelect01">
                      <option v-for="version in leftPanel.versions.available">{{ version }}</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label for="inputGroupSelect02" class="sml">
                      Choose baseline for comparison:
                    </label>
                    <select v-model.number="versions.selectedBaseline" class="custom-select delta-baseline-select" id="inputGroupSelect02">
                      <option v-for="version in leftPanel.versions.available">{{ version }}</option>
                    </select>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-outline-secondary" @click="$emit('close')">Close</button>
                  <button id="show_delta_tree" type="submit" class="btn btn-primary delta-save-button">Save changes</button>
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
import {mapActions, mapGetters} from 'vuex'

export default {
  props: {
    isHidden: Boolean,
    leftPanel: Object
  },
  data () {
    return {
      versions: {
        selectedCurrent: 1,
        selectedBaseline: 1
      }
    }
  },
  async mounted () {
    await this.updateAvailableVersions()
  },
  watch: {
    // TODO remove this watch once the new versioning protocol is implemented in the backend
    'leftPanel.selectedTreeId': async function () {
      await this.updateAvailableVersions()
    }
  },
  computed: {
    ...mapGetters('projects.module', ['getHazards', 'getSafetyArtifactTreeVersions'])
  },
  methods: {
    ...mapActions('projects.module', ['fetchSafetyArtifactTreeVersions']),
    enableDeltaMode () {
      this.leftPanel.deltaMode = true
      this.leftPanel.versions.current = this.versions.selectedCurrent
      this.leftPanel.versions.baseline = this.versions.selectedBaseline
      this.$emit('close')
    },
    async updateAvailableVersions () {
      await this.fetchSafetyArtifactTreeVersions(this.leftPanel.selectedTreeId ? this.leftPanel.selectedTreeId : this.getHazards[0].id)
      this.leftPanel.versions = {
        available: this.getSafetyArtifactTreeVersions,
        current: Math.max(...this.getSafetyArtifactTreeVersions),
        baseline: Math.max(...this.getSafetyArtifactTreeVersions)
      }
      this.versions.selectedCurrent = this.leftPanel.versions.current
      this.versions.selectedBaseline = this.leftPanel.versions.baseline
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
</style>
