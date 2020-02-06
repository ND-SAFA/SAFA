<template>
  <div class="bg-wash border-right" id="sidebar-wrapper">
    <div class="details-panel border-left">
      <div class="list-group list-group-flush">
        <div class="list-group-item bg-wash border-bottom-0 pb-0 sidebar-heading">Hazard Hierarchy</div>
        <div class="list-group-item bg-wash border-top-0 pt-0 sidebar-description">Each leaf hazard contains a
          safety
          tree.</div>

        <ArtifactDetails v-show="!$isEmpty(getSelectedArtifact)" />
        <FaultTreeDetails v-show="false" />
        <DeltaTreeDetails v-show="getDeltaState.enabled && getSelectedTree" />
        <WarningsDetails v-show="!getDeltaState.enabled && getSelectedTree" />

        <div class="list-group-item bg-wash pt-0">
          <p><a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center collapsed" data-toggle="collapse" href="#general-safety" aria-expanded="false">Notation Key <i class="fas fa-chevron-down"></i></a></p>
          <div class="collapse hide" id="general-safety">

            <p class="pl-0 font-weight-bolder">General Safety Tree Notation</p>

            <div class="row no-gutters">
              <div class="col-sm-4">
                <div class="box">
                </div>
              </div>
              <div class="col-sm-8">
                <p>Represents a raw artifact retrieved from the project repository, e.g., hazard,
                  requirements, or test case.</p>
              </div>
            </div>
            <div class="row no-gutters">
              <div class="col-sm-4">
                <div class="box">
                  <i class="fas fa-folder"></i>
                </div>
                <div class="box">
                </div>
              </div>
              <div class="col-sm-8">
                <p>Represents a package retrieved from the project repository that contains source code.</p>
              </div>
            </div>
            <div class="row no-gutters mt-2">
              <div class="col-sm-4">
                <div class="box bg-warning" style="font-size:.8rem">
                  <i class="fas fa-exclamation-triangle"></i> WARNING
                </div>
              </div>
              <div class="col-sm-8">
                <p>Warns that a type of element is completely missing. Can be egregious or nuanced.</p>
              </div>
            </div>

            <p class="mt-2 pl-0 font-weight-bolder">Delta Tree Notation</p>

            <div class="row no-gutters align-items-center">
              <div class="col-sm-4">
                <div class="box">
                </div>
              </div>
              <div class="col-sm-8">
                <p>No change across versions.</p>
              </div>
            </div>
            <div class="row no-gutters align-items-center">
              <div class="col-sm-4">
                <div class="box bg-added-light">
                </div>
              </div>
              <div class="col-sm-8">
                <p>Added to current version.</p>
              </div>
            </div>
            <div class="row no-gutters align-items-center">
              <div class="col-sm-4">
                <div class="box bg-removed-light" style="vertical-align:middle">
                </div>
              </div>
              <div class="col-sm-8">
                <p>Existed in baseline version; deleted from current version.</p>
              </div>
            </div>
            <div class="row no-gutters align-items-center">
              <div class="col-sm-4">
                <div class="box bg-modified-light">
                </div>
              </div>
              <div class="col-sm-8">
                <p>Existed in baseline version; <b>modified</b> in current version.</p>
              </div>
            </div>
          </div> <!-- notation key -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ArtifactDetails from '@/components/Main/RightPanel/ArtifactDetails'
import FaultTreeDetails from '@/components/Main/RightPanel/FaultTreeDetails'
import DeltaTreeDetails from '@/components/Main/RightPanel/DeltaTreeDetails'
import WarningsDetails from '@/components/Main/RightPanel/WarningsDetails'

export default {
  name: 'RightPanel',
  components: { ArtifactDetails, DeltaTreeDetails, FaultTreeDetails, WarningsDetails },
  computed: {
    ...mapGetters('app.module', ['getSelectedArtifact', 'getDeltaState', 'getSelectedTree'])
  }
}
</script>

<style scoped>

</style>
