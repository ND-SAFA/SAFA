/*
*   store/modules/projects.module.js
*/

// import the api endpoints
import projects from '@/api/projects.api'

const TEMP_PROJ_ID = 'spwd.cse.nd.edu'

const state = {
  projects: {
    hazards: []
  }
}

const getters = {
  getHazards (state) {
    return state.projects.hazards
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
  }
}

const mutations = {
  SET_HAZARDS (state, data) {
    state.projects.hazards = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
