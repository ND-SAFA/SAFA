<template>
  <div id="node-list-panel">
    <p class="font-weight-bold text-uppercase mb-2 px-2 d-flex justify-content-between align-items-center">
      Artifact Hierarchy <a href="#" class="text-dark"><i class="fas fa-sync-alt" @click="refreshView"></i></a>
    </p>

    <p class="text-center px-2"><a id="show_node" @click="loadTree(null, null)" class="btn btn-outline-primary btn-sm btn-block text-primary">
      View Hierarchy Tree</a>
    </p>

    <div class="row px-2">
      <div class="col-sm-12">
        <div class="form-group has-search mb-1">
          <i class="fa fa-search form-control-feedback"></i>
          <label class="w-100">
            <input type="text" class="node-search-bar form-control rounded-pill" v-model="searchText" v-on:keyup.esc="searchText = ''" placeholder="Search">
          </label>
        </div>
      </div>
    </div>

    <div class="scroll-nav">
      <ul id="node-list" class="nav">
        <li class="nav-item vw-100" v-for="(item, index) in nodeList" :key="item.id" @click="loadTree(item, index)"  >
          <a class="nav-link" :class="{ active: index === selectedIndex }">
            <div>
              <p class="node-title">{{item.label}} {{item.id}}</p>
              <div v-if="item.data" class="desc" :title="item.data.name">{{$truncate(item.data.name, 40)}}</div>
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
import Vue from 'vue'
import { mapActions, mapGetters } from 'vuex'
import config from 'config'

export default {
  name: 'NodeList',
  data () {
    return {
      selectedIndex: null,
      searchText: '',
      searchFilter: {}
    }
  },
  created () {
    for (const node of this.getNodes) {
      this.searchFilter[node.id] = true
    }
    if (!this.selectedIndex && this.getSelectedTree) {
      this.selectedIndex = this.nodeList.findIndex(h => h.id === this.getSelectedTree)
    }
  },
  computed: {
    ...mapGetters('projects.module', ['getNodes', 'getNodeParents']),
    ...mapGetters('app.module', ['getSelectedTree']),
    nodeList () {
      if (Vue.isEmpty(this.searchFilter)) {
        return this.getNodes
      }
      return this.getNodes.filter(node => this.searchFilter[node.id])
    }
  },
  watch: {
    searchText: async function () {
      if (this.searchText === '') {
        // clear filter
        Object.keys(this.searchFilter).forEach(entry => { this.searchFilter[entry] = true })
      } else {
        const value = this.searchText.toLowerCase()
        const treeId = value.startsWith('uav') ? value : `uav-${value}`
        // TODO implement Vuejs compatible debounce
        await this.fetchProjectNodeParents({treeId, rootType: config.safa_tree.root_node_type})
        for (const node of this.getNodes) {
          this.searchFilter[node.id] = node.data.name.includes(value)
        }
        for (const nodeId of this.getNodeParents) {
          this.searchFilter[nodeId] = true
        }
      }
    }
  },
  methods: {
    ...mapActions('projects.module', ['fetchNodes', 'fetchProjectNodeParents']),
    ...mapActions('app.module', ['setSelectedTree']),
    loadTree (node, index) {
      // load node tree if null arguments are passed
      // otherwise load safety artifact tree
      const selected = node ? node.id : null
      this.setSelectedTree(selected)
      this.selectedIndex = index
    },
    refreshView () {
      this.$parent.$emit('refresh:view')
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
</style>
