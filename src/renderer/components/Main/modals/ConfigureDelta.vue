<template>
  <div class="modal fade delta-modal" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title delta-modal-title" id="exampleModalCenterTitle">Configure Delta</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <form class="delta-form">
          <div class="modal-body">
            <div class="form-group">
              <label for="inputGroupSelect01" class="sml">
                Set current version:
              </label>
              <select class="custom-select delta-current-select" id="inputGroupSelect01">
              </select>
            </div>
            <div class="form-group">
              <label for="inputGroupSelect02" class="sml">
                Choose baseline for comparison:
              </label>
              <select class="custom-select delta-baseline-select" id="inputGroupSelect02">
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>
            <button id="show_delta_tree" type="submit" class="btn btn-primary delta-save-button" data-dismiss="modal" data-root-id="" data-tree-index="0">Save changes</button>
          </div>
        </form>
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