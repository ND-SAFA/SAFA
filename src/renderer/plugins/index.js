import Vue from 'vue'
import truncate from './truncate'
import isEmpty from './is-empty'

const LibraryModule = {
  install (Vue /*, options */) {
    // expose api to components and globals services such as vuex, etc
    Vue.prototype.$truncate = Vue.truncate = truncate
    Vue.prototype.$isEmpty = Vue.isEmpty = isEmpty
    // template filters
    Vue.filter('truncate', truncate)
    Vue.filter('isEmpty', isEmpty)
  }
}

Vue.use(LibraryModule)

export default LibraryModule
