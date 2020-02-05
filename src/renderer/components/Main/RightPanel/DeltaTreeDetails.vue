<template>
  <div class="list-group-item bg-wash pt-0 delta-collapse">
    <p>
      <a class="plain font-weight-bold text-uppercase mt-3 d-flex justify-content-between align-items-center"
              data-toggle="collapse" 
              href="#delta-tree">
        Delta Tree <i class="fas fa-chevron-down"></i>
      </a>
    </p>
    <div class="collapse show" id="delta-tree">
      <div id="change-info">
        <p class="text-uppercase font-weight-bolder">Change Information</p>
        <div v-if="!changeLog.modified.length && !changeLog.added.length && !changeLog.removed.length">
          <p class="font-weight-bolder mb-0">
            <span class="badge badge-pill badge-dark mr-1">&nbsp;</span>
            No Changes
          </p>
          <p class="pl-4">There are no differences between version {{getDeltaState.current}} and version {{getDeltaState.baseline}}</p>
        </div>
        <div v-else>
          <div v-if="changeLog.modified.length">
            <p class="text-uppercase mt-1 text-modified">modified</p>
            <div v-for="(item, idx) in changeLog.modified" :key="idx">
              <div class="d-flex justify-content-between align-items-center">
                <p class="font-weight-bolder mb-0">
                  <span class="badge badge-pill bg-modified text-white mr-1">{{item.changeIndex}}</span>
                  {{item.type}} {{item.id}}
                </p>
                <Rank />
              </div>
              <p>{{getName(item)}}</p>
            </div>
          </div>
          <div v-if="changeLog.added.length">
            <p class="text-uppercase mt-1 text-added">added</p>
            <div v-for="(item, idx) in changeLog.added" :key="idx">
              <div class="d-flex justify-content-between align-items-center">
                <p class="font-weight-bolder mb-0">
                  <span class="badge badge-pill bg-added text-white mr-1">{{item.changeIndex}}</span>
                  {{item.type}} {{item.id}}
                </p>
                <Rank />
              </div>
              <p>{{getName(item)}}</p>
            </div>
          </div>
          <div v-if="changeLog.removed.length">
            <p class="text-uppercase mt-1 text-removed">removed</p>
            <div v-for="(item, idx) in changeLog.removed" :key="idx">
              <div class="d-flex justify-content-between align-items-center">
                <p class="font-weight-bolder mb-0">
                  <span class="badge badge-pill bg-removed text-white mr-1">{{item.changeIndex}}</span>
                  {{item.type}} {{item.id}}
                </p>
                <Rank />
              </div>
              <p>{{getName(item)}}</p>
            </div>
          </div>
        </div>
      </div> 
    </div> 
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Rank from '@/components/Main/RightPanel/DeltaTreeDetails/Rank'

export default {
  name: 'DeltaTreeDetails',
  components: { Rank },
  computed: {
    ...mapGetters('app.module', ['getDeltaTreeChangeLog', 'getDeltaState']),
    changeLog () {
      return JSON.parse(JSON.stringify(this.getDeltaTreeChangeLog))
    }
  },
  methods: {
    getName (item) {
      if (item.type === 'Package') {
        return item.id
      } else if (item.type === 'Code') {
        return item.id.split('/').pop()
      } else {
        return item.name
      }
    }
  }
}
</script>

<style scoped>

</style>