<template>
  <div id="fta-list-panel">
    <p class="font-weight-bold text-uppercase mb-2 px-2 d-flex justify-content-between align-items-center">
      Fault Trees
    </p>

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
</template>

<script>
export default {
  name: 'FTANodeList'
}
</script>

<style scoped>

</style>
