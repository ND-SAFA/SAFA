<template>
  <div id="hazard-list-panel">
    <div class="row px-2">
      <div class="col-sm-12">
        <div class="form-group has-search mb-1">
          <i class="fa fa-search form-control-feedback"></i>
          <label class="w-100">
            <input type="text" class="hazard-search-bar form-control rounded-pill" v-model="searchText" v-on:keyup.esc="searchText = ''" placeholder="Search">
          </label>
        </div>
      </div>
    </div>

    <div id="scroll-nav">
      <ul id="hazard-list" class="nav">
        <li class="nav-item vw-100" v-for="(item, index) in Object.keys(artifactData)" :key="item.id">
          <a class="nav-link" :class="{ active: index === selectedIndex }" @click="onClickArtifact(index)">
            <div>
              <p class="hazard-title">{{item}}{{index}}</p>
              <div class="desc" :title="artifactData[item].desc">{{$truncate(artifactData[item].desc, 40)}}</div>
            </div>
            <span v-if="item.warnings" class="badge badge-pill badge-warning px-1">
              <i class="fas fa-exclamation-triangle"></i>
            </span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'SourceLinksList',

  props: {
    artifactData: Object
  },

  data () {
    return {
      selectedIndex: 0,
      searchText: '',
      searchFilter: {}
    }
  },

  computed: {
    ...mapGetters('projects.module', ['getHazards', 'getNodeParents']),
    ...mapGetters('app.module', ['getSelectedTree'])
  },

  methods: {
    ...mapActions('projects.module', ['fetchHazards', 'fetchProjectNodeParents']),
    ...mapActions('app.module', ['setSelectedTree']),
    onClickArtifact (event) {
      console.log('emitting event: ', event)
      this.selectedIndex = event
      this.$emit('artifact-chosen', event)
    }
  }
}
</script>

<style scoped>
  p {
    line-height: 1.3rem;
  }

  .desc {
    font-size: .7rem;
    margin-bottom: 0;
    width: 15rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .nav-link {
    display: flex;
    align-items: center;
    padding: .75rem 1rem;
  }

  .nav-link div {
    width: 95%;
    float: left;
  }

  .badge {
    float: right;
    width: 10%;
  }

  #scroll-nav {
    height: calc(100vh - 296px);
    overflow-x: hidden;
    overflow-y: auto;
  }
</style>
