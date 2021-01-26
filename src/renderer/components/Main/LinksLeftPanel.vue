<template>
  <div id="left-list-view" class="p-0 bg-light">
    <div class="d-flex flex-column pt-0 px-2 mb-0">
      <p class="font-weight-bold text-uppercase mb-2 mt-2 px-2 d-flex justify-content-between align-items-center">
        Source Type<a href="#" class="text-dark"></a>
      </p>
        <select class="custom-select mb-3" id="inputGroupSelect01" v-model="selected">
          <option v-for="source in sourceTypes" :key="source.id" v-bind:value="{ item: source }">{{source}}</option>
        </select>
      <p class="font-weight-bold text-uppercase mb-2 mt-2 px-2 d-flex justify-content-between align-items-center">
        Target Type<a href="#" class="text-dark"></a>
      </p>
        <select class="custom-select" id="inputGroupSelect01">
          <option v-for="target in linkData[selected.item]" :key="target.id">{{target}}</option>
        </select>
        <button type="button" class="btn btn-primary btn-sm mb-3">
        Fetch Links
      </button>
    </div>

    <SourceLinksList />

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SourceLinksList from '@/components/Main/LeftPanel/SourceLinksList'

export default {
  name: 'LinksLeftPanel',

  props: {
    typeData: Object
  },

  data () {
    return {
      deltaEnabled: false,
      showTab: 'Artifacts',
      sourceTypes: {},
      linkData: {},
      selected: ''
    }
  },

  components: { SourceLinksList },

  mounted () {
    this.sourceTypes = Object.keys(this.typeData.data)
    this.linkData = this.typeData.data
  },

  computed: {
    ...mapGetters('projects.module', ['getLinkTypes'])
  }
}
</script>

<style scoped>
.custom-switch label {
  font-size: 0.9rem;
  padding-top: 0.1rem;
}
</style>
