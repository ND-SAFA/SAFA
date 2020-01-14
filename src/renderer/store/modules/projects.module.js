/*
*   store/modules/projects.module.js
*/

// import the api endpoints
import projects from '@/api/projects.api'

const TEMP_PROJ_ID = 'spwd.cse.nd.edu'

const state = {
  projects: {
    hazards: [],
    hazardTree: []
  }
}

const getters = {
  getHazards (state) {
    return state.projects.hazards
  },

  getHazardTree (state) {
    return state.projects.hazardTree
  }
}

const actions = {
  async fetchHazards ({ commit }) {
    try {
      const response = await projects.getProjectHazards(TEMP_PROJ_ID)
      commit('SET_HAZARDS', response)
    } catch (error) {
      // handle the error here
    }
  },

  async fetchHazardTree ({ commit }) {
    try {
      const response = await projects.getProjectHazardTree(TEMP_PROJ_ID)
      commit('SET_HAZARD_TREE', response)
    } catch (error) {
    }
  }
}

const mutations = {
  SET_HAZARDS (state, data) {
    state.projects.hazards = data
  },

  SET_HAZARD_TREE (state, data) {
    state.projects.hazardTree = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
