import Vue from 'vue'
import truncate from './truncate'
import isEmpty from './is-empty'
import capitalize from './capitalize'

const LibraryModule = {
  install (Vue /*, options */) {
    // expose api to components and globals services such as vuex, etc
    Vue.prototype.$truncate = Vue.truncate = truncate
    Vue.prototype.$isEmpty = Vue.isEmpty = isEmpty
    Vue.prototype.$capitalize = Vue.capitalize = capitalize
    // template filters
    Vue.filter('truncate', truncate)
    Vue.filter('isEmpty', isEmpty)
    Vue.filter('capitalize', capitalize)
  }
}

Vue.use(LibraryModule)

export default LibraryModule
