<template>
  <div v-if="nodesWithWarnings.length > 0" class="list-group-item bg-wash pt-0 warnings-collapse">
    <p>
      <a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" 
              data-toggle="collapse" 
              data-target=".warnings-info" 
              href="#">
        WARNINGS <i class="fas fa-chevron-down"></i>
      </a>
    </p>
    <div class="warnings-info collapse show">
      <div v-for="(node, i) in nodesWithWarnings" :key="i">
        <div v-for="(warning, j) in node.data.warnings" :key="j">
          <p class="font-weight-bolder mb-0">
            <span class="badge badge-pill badge-warning px-1">
              <i class="fas fa-exclamation-triangle"></i>
            </span> {{$capitalize(node.data.type)}} {{node.data.id.toUpperCase()}}
          </p>
          <p>{{warning}}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'WarningsDetails',
  computed: {
    ...mapGetters('projects.module', ['getSafetyArtifactTree']),
    nodesWithWarnings () {
      if (!(this.getSafetyArtifactTree instanceof Array) || this.getSafetyArtifactTree.length === 0) {
        return []
      }
      return this.getSafetyArtifactTree.filter(element => element.data.warnings)
    }
  }
}
</script>

<style scoped>

</style>