/*
*   store/modules/app.module.js
*/

// Applications local cache

const state = {
  app: {
    delta: {
      enabled: false,
      baseline: 0,
      current: 0
    }
  }
}

const getters = {
  getDeltaState (state) {
    return state.app.delta
  }
}

const actions = {
  updateDelta ({ commit }, delta) {
    commit('UPDATE_DELTA', delta)
  }
}

const mutations = {
  UPDATE_DELTA (state, data) {
    if (data.baseline > data.current) {
      const swap = data.current
      data.current = data.baseline
      data.baseline = swap
    }
    state.app.delta = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
