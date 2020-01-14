<template>
  <div id="hazard-list-panel">
    <p class="font-weight-bold text-uppercase mb-2 px-2 d-flex justify-content-between align-items-center">
      Hazard Hierarchy <a href="#" class="text-dark"><i class="fas fa-sync-alt"></i></a>
    </p>

    <p class="text-center px-2"><a id="show_hazard" class="btn btn-outline-primary btn-sm btn-block text-primary">
      View Hazard Tree</a>
    </p>

    <div class="row px-2">
      <div class="col-sm-12">
        <div class="form-group has-search mb-1">
          <i class="fa fa-search form-control-feedback"></i>
          <label class="w-100">
            <input type="text" class="hazard-search-bar form-control rounded-pill" placeholder="Search">
          </label>
        </div>
      </div>
    </div>

    <div class="scroll-nav">
      <ul id="hazard-list" class="nav">
        <li class="nav-item vw-100" v-for="item in getHazards" :key="item.id" @click="loadTree(item)">
          <a class="nav-link">
            <div>
              <p class="hazard-title">{{item.label}} {{item.id}}</p>
              <div v-if="item.data" class="desc" >{{$truncate(item.data.name)}}</div>
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
  computed: {
    ...mapGetters('projects.module', ['getHazards'])
  },
  methods: {
    ...mapActions('projects.module', ['fetchHazards']),
    loadTree (hazard) {
      console.log(hazard)
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