<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  import AppMenu from '@/menu'

  export default {
    name: 'safa-vue',
    data () {
      return {
        myData: 10
      }
    },
    created () {
      AppMenu.findMenuItemById('project.sync').click = this.projectSync.bind(this)
      AppMenu.findMenuItemById('project.freeze').click = this.projectFreeze.bind(this)
      AppMenu.setApplicationMenu()
    },
    methods: {
      projectSync () {
        console.log('projectSync()')
      },
      projectFreeze () {
        console.log('projectFreeze()')
      }
    }
  }
</script>

<style>
  /* CSS */
</style>
