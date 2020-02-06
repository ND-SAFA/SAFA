<template>
  <ul class="navbar-nav ma sync-notif" style="">
    <li class="navbar-text mr-1">Synchronizing With Project Repository</li>
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
  computed: {
    ...mapGetters('projects.module', ['getSyncProgress']),
    percentComplete () {
      return `w-${25 + (25 * this.getSyncProgress)}`
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