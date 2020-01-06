<template>
  <header>
    <nav id="navbar" class="navbar fixed-top navbar-expand-md navbar-dark bg-dark">
      <a id="logo" class="navbar-brand" href="#">Safety Forest</a>
      <ul class="navbar-nav mr-auto">
        <li class="navbar-text">Desktop App</li>
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
export default {
  props: {
    rightPanel: {}
  },
  methods: {
    menuToggled () {
      this.rightPanel.isHidden = !this.rightPanel.isHidden
    }
  }
}
</script>

<style scoped>

</style>