/*
*   store/modules/projects.module.js
*/

// import the api endpoints
import projects from '@/api/projects.api'

const TEMP_PROJ_ID = 'spwd.cse.nd.edu'

const state = {
  projects: {
    hazards: [],
    hazardTree: [],
    safetyArtifactTree: []
  }
}

const getters = {
  getHazards (state) {
    return state.projects.hazards
  },

  getHazardTree (state) {
    return state.projects.hazardTree
  },

  getSafetyArtifactTree: (state) => {
    return state.projects.safetyArtifactTree
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
  },

  async fetchSafetyArtifactTree ({ commit }, treeId) {
    try {
      const response = await projects.getProjectSafetyArtifactTree(TEMP_PROJ_ID, treeId)
      commit('SET_SAFETY_ARTIFACT_TREE', response)
    } catch (error) {
      // handle the error here
    }
  }
}

const mutations = {
  SET_HAZARDS (state, data) {
    state.projects.hazards = data
  },

  SET_HAZARD_TREE (state, data) {
    state.projects.hazardTree = data
  },

  SET_SAFETY_ARTIFACT_TREE (state, data) {
    state.projects.safetyArtifactTree = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
