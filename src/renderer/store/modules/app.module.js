/*
*   store/modules/app.module.js
*/

// Applications local cache
import Vue from 'vue'

const state = {
  app: {
    delta: {
      enabled: false,
      baseline: 0,
      current: 0,
      changeLog: {
        added: [], modified: [], removed: []
      }
    },
    selectedArtifact: null,
    selectedTree: null
  }
}

const getters = {
  getDeltaState (state) {
    return state.app.delta
  },

  getSelectedArtifact (state) {
    return state.app.selectedArtifact
  },

  getSelectedTree (state) {
    return state.app.selectedTree
  },

  getDeltaTreeChangeLog (state) {
    return state.app.delta.changeLog
  }
}

const actions = {
  updateDelta ({ commit }, delta) {
    commit('UPDATE_DELTA', delta)
  },

  setSelectedArtifact ({ commit }, artifact) {
    commit('SET_SELECTED_ARTIFACT', artifact)
  },

  setSelectedTree ({ commit }, tree) {
    commit('SET_SELECTED_TREE', tree)
  },

  setDeltaTreeChangeLog ({ commit }, log) {
    commit('SET_DELTA_TREE_CHANGE_LOG', log)
  }
}

const mutations = {
  UPDATE_DELTA (state, data) {
    if (data.current > data.baseline) {
      const swap = data.current
      data.current = data.baseline
      data.baseline = swap
    }
    data.changed = Date.now()
    state.app.delta = data
  },

  SET_SELECTED_ARTIFACT (state, data) {
    state.app.selectedArtifact = data
  },

  SET_SELECTED_TREE (state, data) {
    state.app.selectedTree = data
  },

  SET_DELTA_TREE_CHANGE_LOG (state, data) {
    if (Vue.isEmpty(data)) {
      data = { added: [], modified: [], removed: [] }
    }
    state.app.delta.changeLog = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
