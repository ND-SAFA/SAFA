<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  import AppMenu from '@/menu'
  import { shell } from 'electron'

  export default {
    name: 'safa-vue',
    data () {
      return {
        myData: 10
      }
    },
    computed: {
      ...mapGetters('projects.module', ['getSyncProgress'])
    },
    created () {
      AppMenu.findMenuItemById('project.sync').click = this.projectSync.bind(this)
      AppMenu.findMenuItemById('project.freeze').click = this.projectFreeze.bind(this)
      AppMenu.findMenuItemById('project.help').click = this.getHelp.bind(this)
      AppMenu.setApplicationMenu()
    },
    methods: {
      ...mapActions('projects.module', ['saveProjectVersion', 'syncProject', 'clearFiles']),
      async projectSync () {
        try {
          await this.syncProject()
        } catch (e) {

        }
      },
      async projectFreeze () {
        await this.saveProjectVersion()
      },
      getHelp () {
        shell.openExternal('https://github.com/SAREC-Lab/SAFA-Documentation')
      }
    }
  }
</script>

<style>
  /* CSS */
</style>
