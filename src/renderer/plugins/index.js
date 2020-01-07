import Vue from 'vue'
import truncate from './truncate'

const LibraryModule = {
  install (Vue /*, options */) {
    // expose api to components and globals services such as vuex, etc
    Vue.prototype.$truncate = Vue.truncate = truncate
    // template filters
    Vue.filter('truncate', truncate)
  }
}

Vue.use(LibraryModule)

export default LibraryModule
