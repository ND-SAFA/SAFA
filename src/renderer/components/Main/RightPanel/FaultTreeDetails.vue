<template>
  <div class="d-none list-group-item bg-wash pt-0" id="fta-node-details">
    <p>
      <a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" 
              data-toggle="collapse" 
              href="#fta-node-details-content" 
              aria-expanded="false">
        Selected FTA Node <i class="fas fa-chevron-down"></i>
      </a>
    </p>
    <div class="collapse show" id="fta-node-details-content"></div>
  </div>
</template>

<script>
export default {
  name: 'FaultTreeDetails'
}
</script>

<style scoped>

</style>