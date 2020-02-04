<template>
  <header>
    <nav id="navbar" class="navbar fixed-top navbar-expand-md navbar-dark bg-dark px-1">
      <ul class="navbar-nav">
        <li class="nav-item pr-1">
          <a id="left-menu-toggle" class="btn btn-outline-light active" data-toggle="button" aria-pressed="true" href="#"><i class="fas fa-bars"></i></a>
        </li>
        <li id="logo" class="navbar-brand">Safety Forest</li>
      </ul>
      <ul class="navbar-nav mr-auto">
        <li class="navbar-text mr-5">Desktop App</li>
        <li class="navbar-text delta-version-indicator ml-1 mr-1" v-show="this.getDeltaState.enabled"><i class="fas fa-play fa-rotate-270"></i> <span class="font-weight-bold">Current:</span> <span id="delta-current-indicator">{{ current }}</span></li>
        <li class="navbar-text delta-version-indicator mx-1" v-show="this.getDeltaState.enabled"><span class="font-weight-bold">Baseline:</span> <span id="delta-baseline-indicator">{{ baseline }}</span></li>
      </ul>
      <ul class="navbar-nav left">
        <li class="nav-item active">
          <a @click="menuToggled" class="btn btn-outline-light" href="#"><i class="fas fa-bars"></i></a>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'HeaderNav',
  props: {
    rightPanel: Object
  },
  methods: {
    menuToggled () {
      this.rightPanel.isHidden = !this.rightPanel.isHidden
    }
  },
  computed: {
    ...mapGetters('app.module', ['getDeltaState']),
    current () {
      return Math.max(this.getDeltaState.current, this.getDeltaState.baseline)
    },
    baseline () {
      return Math.min(this.getDeltaState.current, this.getDeltaState.baseline)
    }
  }
}
</script>

<style scoped>

</style>
