<template>
  <div id="left-list-view" class="p-0 bg-light">
    <div class="d-flex flex-column pt-0 px-2 mb-0">
      <p class="font-weight-bold text-uppercase mb-2 mt-2 px-2 d-flex justify-content-between align-items-center">
        Source Type<a href="#" class="text-dark"></a>
      </p>
        <select class="custom-select" id="inputGroupSelect01" v-model="sourceSelected">
          <option v-for="source in sourceTypes" :key="source.id" v-bind:value="{ item: source }">{{source}}</option>
        </select>
      <p class="font-weight-bold text-uppercase mb-2 mt-2 px-2 d-flex justify-content-between align-items-center">
        Target Type<a href="#" class="text-dark"></a>
      </p>
        <select class="custom-select mb-3" id="inputGroupSelect01" v-model="targetSelected">
          <option v-for="target in linkData[sourceSelected.item]" :key="target.id">{{target}}</option>
        </select>
        <button type="button" class="btn btn-primary btn-sm mb-3" @click="requestLinkData">
        Fetch Links
      </button>
    </div>

    <SourceLinksList :artifact-data="artifactData" :chosen-artifact="artifactChosen" @artifact-chosen="chooseArtifact"/>

  </div>
</template>

<script>
import { mapActions } from 'vuex'
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
      artifactData: {},
      sourceSelected: '',
      targetSelected: '',
      artifactChosen: 0
    }
  },

  components: { SourceLinksList },

  mounted () {
    this.sourceTypes = Object.keys(this.typeData.data)
    this.linkData = this.typeData.data
    console.log(this.linkData)
  },

  watch: {
    update () {
      console.log('watching for new index: ', this.artifactChosen)
    }
  },

  computed: {
    ...mapActions('projects.module', ['getApproverData'])
  },

  methods: {
    requestLinkData () {
      var selectedDict = {
        'source': this.sourceSelected.item,
        'target': this.targetSelected
      }
      console.log(selectedDict)
      this.getApproverData.then(result => {
        this.artifactData = result.data
        this.$emit('artifact-data', this.artifactData)
      })
    },
    chooseArtifact (result) {
      console.log('new artifact chosen? ', result)
      this.artifactChosen = result
      this.$emit('chosen-artifact', result)
    }
  }
}
</script>