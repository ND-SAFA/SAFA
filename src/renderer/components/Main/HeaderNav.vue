<template>
  <header>
    <nav id="navbar" class="navbar fixed-top navbar-expand-md navbar-dark bg-dark px-1">
      <ul class="navbar-nav">
        <li class="nav-item pr-1">
          <a @click="ltMenuToggled" class="btn btn-outline-light" href="#"><i :class="ltMenuToggleClass"></i></a>
        </li>
        <li id="logo" class="navbar-brand">Safety Forest</li>
      </ul>
      <ul class="navbar-nav mr-auto">
        <li class="navbar-text mr-5">Desktop App</li>
        <li class="navbar-text delta-version-indicator ml-1 mr-1" v-show="this.getDeltaState.enabled"><i class="fas fa-play fa-rotate-270"></i> <span class="font-weight-bold">Current:</span> <span id="delta-current-indicator">{{ current }}</span></li>
        <li class="navbar-text delta-version-indicator mx-1" v-show="this.getDeltaState.enabled"><span class="font-weight-bold">Baseline:</span> <span id="delta-baseline-indicator">{{ baseline }}</span></li>
      </ul>
      <ProgressBar :status-type="statusType" v-show="syncInProgress || generateInProgress"/>
      <ul class="navbar-nav left">
        <li class="nav-item active">
          <a @click="rtMenuToggled" class="btn btn-outline-light" href="#"><i :class="rtMenuToggleClass"></i></a>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import { mapGetters } from 'vuex'
import ProgressBar from '@/components/Main/HeaderNav/ProgressBar'

export default {
  name: 'HeaderNav',
  components: { ProgressBar },
  props: {
    rightPanel: Object,
    leftPanel: Object
  },
  data () {
    return {
      statusType: null
    }
  },
  methods: {
    rtMenuToggled () {
      this.rightPanel.isHidden = !this.rightPanel.isHidden
      this.$emit('resize:view')
    },
    ltMenuToggled () {
      this.leftPanel.isHidden = !this.leftPanel.isHidden
      this.$emit('resize:view')
    }
  },
  computed: {
    ...mapGetters('app.module', ['getDeltaState']),
    ...mapGetters('projects.module', ['getSyncProgress', 'getGenerateProgress']),
    syncInProgress () {
      if (this.getSyncProgress > -1) {
        console.log('syncing fr fr ')
        this.statusType = 'sync'
      }
      return this.getSyncProgress > -1
    },
    generateInProgress () {
      if (this.getGenerateProgress > -1) {
        console.log('generating links')
        this.statusType = 'generate'
      }
      return this.getGenerateProgress > -1
    },
    current () {
      return Math.max(this.getDeltaState.current, this.getDeltaState.baseline)
    },
    baseline () {
      return Math.min(this.getDeltaState.current, this.getDeltaState.baseline)
    },
    rtMenuToggleClass () {
      const chevron = this.rightPanel.isHidden ? 'left' : 'right'
      return `fas fa-chevron-${chevron}`
    },
    ltMenuToggleClass () {
      const chevron = this.leftPanel.isHidden ? 'right' : 'left'
      return `fas fa-chevron-${chevron}`
    }
  }
}
</script>

<style scoped>

</style>
