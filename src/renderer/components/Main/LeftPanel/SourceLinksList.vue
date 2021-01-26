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
        <li class="nav-item vw-100" v-for="(item, index) in Object.keys(artifacts)" :key="item.id" >
          <a class="nav-link" :class="{ active: index === selectedIndex }">
            <div>
              <p class="hazard-title">{{item}}</p>
              <div class="desc" :title="artifacts[item].description">{{$truncate(artifacts[item].description, 40)}}</div>
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
  name: 'HazardList',
  data () {
    return {
      selectedIndex: null,
      searchText: '',
      searchFilter: {},
      artifacts: { 'UAV-10': {'description': 'This is a test description'}, 'UAV-11': {'description': 'This is a test description'}, 'UAV-12': {'description': 'This is a test description'}, 'UAV-13': {'description': 'This is a test description'}, 'UAV-14': {'description': 'This is a test description'} }
    }
  },
  computed: {
    ...mapGetters('projects.module', ['getHazards', 'getNodeParents']),
    ...mapGetters('app.module', ['getSelectedTree'])
  },
  methods: {
    ...mapActions('projects.module', ['fetchHazards', 'fetchProjectNodeParents']),
    ...mapActions('app.module', ['setSelectedTree'])
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
    overflow-y: scroll;
  }
</style>
