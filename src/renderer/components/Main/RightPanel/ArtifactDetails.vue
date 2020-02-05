<template>
  <div class="list-group-item bg-wash pt-0">
    <p>
      <a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center" 
              data-toggle="collapse" 
              href="#node-details-content" 
              aria-expanded="false">
        Selected Node <i class="fas fa-chevron-down"></i>
      </a>
    </p>
    <div class="collapse show" id="node-details-content">
      <p v-if="!!artifact.type && !!artifact.id" class="font-weight-bolder pl-0 selected-artifact">{{$capitalize(artifact.type)}} {{artifact.id.toUpperCase()}}</p>
      <p v-if="!!artifact.name" class="pl-0 selected-artifact">{{artifact.name}}</p>
      <div v-if="!!artifact.source && !!artifact.href && artifact.source !== '' && artifact.href !== ''" 
            class="row">
        <p class="col-sm-2 font-weight-bolder selected-artifact">Source</p>
        <p class="col-sm-10 selected-artifact">
          <a href="#" @click="clickLink(artifact.href)">{{$capitalize(artifact.source)}}</a>
        </p>
      </div>
      <div v-if="!!artifact.description && artifact.description !== ''">
        <div class="row">
          <p class="col-sm-12 font-weight-bolder selected-artifact">Description</p>
        </div>
        <div class="description-content row">
          <p class="col-sm-12 selected-artifact">{{artifact.description}}</p>
        </div>
      </div>
      <div v-if="!!artifact.status && artifact.status !== ''" class="row">
        <p class="col-sm-2 font-weight-bolder selected-artifact">Status</p>
        <p class="col-sm-10 selected-artifact">{{artifact.status}}</p>
      </div>
      <button v-if="!!artifact.type && artifact.type.toUpperCase() === 'HAZARD'" class="btn btn-outline-secondary btn-sm btn-block" type="button">
        View Safety Artifact Tree
      </button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'ArtifactDetails',
  computed: {
    ...mapGetters('app.module', ['getSelectedArtifact']),
    artifact () {
      return this.getSelectedArtifact
    }
  },
  methods: {
    clickLink (link) {
      this.$parent.$emit('open:link', link)
    }
  }
}
</script>

<style scoped>

</style>