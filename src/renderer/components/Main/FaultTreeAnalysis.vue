<template>
  <div id="center-panel-2" role="tabpanel" aria-labelledby="fault-tree-tab" class="fade col d-none graph-view p-0">
    <div id="cy-fta-error" class="alert alert-warning alert-dismissible fade show" role="alert" style="display:none">
      <span id="cy-fta-error-text">Problem Rendering the FTA.</span>
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <div id="cy-fta-parent">
      <div id="cy-fta"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FaultTreeAnalysis'
}
</script>

<style scoped>

</style>