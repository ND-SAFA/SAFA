/*
*   store/modules/app.module.js
*/

// Electron App Data

const state = {
  app: {
    menu: Object()
  }
}

const getters = {
  getAppMenu (state) {
    return state.app.menu
  }
}

const actions = {
  async updateApplicationMenu ({ commit }, menu) {
    commit('UPDATE_APPLICATION_MENU', menu)
  }
}

const mutations = {
  UPDATE_APPLICATION_MENU (state, data) {
    state.app.menu = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
