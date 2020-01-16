<template>
  <div class="bg-wash border-right" v-show="!isHidden" id="sidebar-wrapper">
    <div class="details-panel border-left">
      <div class="list-group list-group-flush">
        <div class="list-group-item bg-wash border-bottom-0 pb-0 sidebar-heading">Hazard Hierarchy</div>
        <div class="list-group-item bg-wash border-top-0 pt-0 sidebar-description">Each leaf hazard contains a
          safety
          tree.</div>

        <!--Artifact details-->
        <div class="d-none list-group-item bg-wash pt-0" id="node-details">
          <p><a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" data-toggle="collapse" href="#node-details-content" aria-expanded="false">Selected Node <i class="fas fa-chevron-down"></i></a></p>
          <div class="collapse show" id="node-details-content">
          </div>
        </div>
        <!--End Artifact details-->

        <!--FTA Node details-->
        <div class="d-none list-group-item bg-wash pt-0" id="fta-node-details">
          <p><a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" data-toggle="collapse" href="#fta-node-details-content" aria-expanded="false">Selected FTA Node <i class="fas fa-chevron-down"></i></a></p>
          <div class="collapse show" id="fta-node-details-content">
          </div>
        </div>
        <!--End FTA Node details-->

        <div class="list-group-item bg-wash pt-0 delta-collapse d-none">
          <p><a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" data-toggle="collapse" href="#delta-tree">Delta Tree <i class="fas fa-chevron-down"></i></a></p>
          <div class="collapse show" id="delta-tree">
            <div id="change-info">
            </div> <!-- change-info -->
          </div> <!-- delta-tree -->
        </div>

        <div class="list-group-item bg-wash pt-0 warnings-collapse d-none">
          <p><a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" data-toggle="collapse" data-target=".warnings-info" href="#">WARNINGS <i class="fas fa-chevron-down"></i></a></p>
          <div class="warnings-info collapse show">
          </div> <!-- warnings-info -->
        </div>

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
export default {
  name: 'RightPanel',
  props: {
    isHidden: true
  }
}
</script>

<style scoped>

</style>
