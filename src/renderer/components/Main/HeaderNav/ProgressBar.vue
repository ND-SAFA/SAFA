<template>
  <ul class="navbar-nav ma sync-notif" style="">
    <li v-if="statusType === 'sync'" class="navbar-text mr-1">Synchronizing With Project Repository</li>
    <li v-else class="navbar-text mr-1">Generating Trace Links</li>
    <li class="navbar-text mr-5">
      <div class="progress">
        <div v-bind:class="[progressBar, percentComplete]"></div>
      </div>
    </li>
  </ul>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ProgressBar',
  props: {
    statusType: String
  },
  computed: {
    ...mapGetters('projects.module', ['getSyncProgress', 'getGenerateProgress']),
    percentComplete () {
      if (this.statusType === 'sync') {
        return `w-${25 + (25 * this.getSyncProgress)}`
      } else {
        console.log(this.getGenerateProgress)
        return `w-${100 * this.getGenerateProgress}`
      }
    }
  },
  data () {
    return {
      progressBar: 'progress-bar progress-bar-striped bg-success progress-bar-animated'
    }
  }
}
</script>

<style scoped>
  .progress {
    width: 200px
  }
</style>