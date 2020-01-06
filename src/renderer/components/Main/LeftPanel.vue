<template>
  <div id="left-list-view" class="p-0 bg-light">
    <p class="text-center pt-3 px-2 bg-wash mb-0">
      <button type="button" class="btn btn-outline-secondary btn-sm btn-block" data-toggle="modal" data-target="#exampleModalCenter">
        Configure Delta
      </button>
    </p>

    <ul id="top-tabs" role="tablist" class="nav nav-tabs nav-fill pt-3 mb-3 bg-wash">
      <li class="nav-item">
        <a class="nav-link active" id="artifact-tree-tab" data-toggle="tab" href="#center-panel" role="tab" aria-controls="center-panel" aria-selected="true">Artifacts</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" id="fault-tree-tab" data-toggle="tab" href="#center-panel-2" role="tab" aria-controls="center-panel-2" aria-selected="false">Safety Model</a>
      </li>
    </ul>

    <div id="hazard-list-panel" role="tabpanel" aria-labelledby="artifact-tree-tab" class="">
      <p class="font-weight-bold text-uppercase mb-2 px-2 d-flex justify-content-between align-items-center">
        Hazard
        Hierarchy <a href="#" class="text-dark"><i class="fas fa-sync-alt"></i></a></p>

      <p class="text-center px-2"><a id="show_hazard" class="btn btn-outline-primary btn-sm btn-block text-primary">View
          Hazard Tree</a></p>

      <div class="row px-2">
        <div class="col-sm-12">
          <div class="form-group has-search mb-1">
            <i class="fa fa-search form-control-feedback"></i>
            <label class="w-100">
              <input type="text" class="hazard-search-bar form-control rounded-pill" placeholder="Search">
            </label>
          </div>
        </div>
      </div>

      <div class="scroll-nav">
        <ul id="hazard-list" class="nav"></ul>
      </div>
    </div>

    <div id="fta-list-panel" role="tabpanel" aria-labelledby="fault-tree-tab" class="d-none">
      <p class="font-weight-bold text-uppercase mb-2 px-2 d-flex justify-content-between align-items-center">
        Fault Trees </p>

      <div class="row px-2">
        <div class="col-sm-12">
          <div class="form-group has-search mb-1">
            <i class="fa fa-search form-control-feedback"></i>
            <label class="w-100">
              <input type="text" class="fta-search-bar form-control rounded-pill" placeholder="Search">
            </label>
          </div>
        </div>
      </div>

      <div class="scroll-nav">
        <ul id="fta-list" class="nav"></ul>
      </div>

    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>

</style>