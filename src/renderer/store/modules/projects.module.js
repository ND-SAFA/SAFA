/*
*   store/modules/projects.module.js
*/

// import the api endpoints
import projects from '@/api/projects.api'

const TEMP_PROJ_ID = 'spwd.cse.nd.edu'

const state = {
  projects: {
    delta: {
      trees: []
    },
    versions: {
      latest: 0
    },
    hazards: [],
    hazardTree: [],
    safetyArtifactTree: [],
    node: {
      parents: []
    }
  }
}

const getters = {
  getHazards (state) {
    return state.projects.hazards
  },

  getHazardTree (state) {
    return state.projects.hazardTree
  },

  getSafetyArtifactTree (state) {
    return state.projects.safetyArtifactTree
  },

  getNodeParents (state) {
    return state.projects.node.parents
  },

  getProjectVersions (state) {
    return state.projects.versions
  },

  getDeltaTrees (state) {
    return state.projects.delta.trees
  }
}

const actions = {
  async fetchHazards ({ commit }) {
    try {
      const response = await projects.getProjectHazards(TEMP_PROJ_ID)
      // Fetch hazard warnings at the same time
      const warnings = await projects.getProjectHazardsWarnings(TEMP_PROJ_ID)
      // Store warnings in corresponding hazard
      for (const hazard of response) {
        hazard.warnings = warnings[hazard.id]
      }
      commit('SET_HAZARDS', response)
    } catch (error) {
      // TODO(Adam): handle the error here
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
      // TODO(Adam): handle the error here
    }
  },

  async fetchProjectVersions ({ commit }) {
    try {
      const response = await projects.getProjectVersions(TEMP_PROJ_ID)
      commit('SET_PROJECT_VERSIONS', response)
    } catch (error) {
      // TODO(Adam): handle the error here
    }
  },

  async saveProjectVersion ({ commit }) {
    try {
      const response = await projects.postProjectVersion(TEMP_PROJ_ID)
      console.log(response)
      commit('SET_PROJECT_VERSIONS', response)
    } catch (e) {
      // TODO(Adam): handle the error here
    }
  },

  async fetchProjectNodeParents ({ commit }, nodeId) {
    try {
      const response = await projects.getProjectNodeParents(TEMP_PROJ_ID, nodeId)
      commit('SET_NODE_PARENTS', response)
    } catch (error) {
      // TODO(Adam): handle the error here
    }
  },

  async fetchDeltaTrees ({ commit }, payload) {
    const { treeId, baseline, current } = payload
    try {
      const response = await projects.getDeltaTrees(TEMP_PROJ_ID, treeId, [baseline, current])
      console.log(response)
      commit('SET_DELTA_TREES', response)
    } catch (e) {
      // TODO(Adam): handle error
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
  },

  SET_PROJECT_VERSIONS (state, data) {
    state.projects.versions = data
  },

  SET_NODE_PARENTS (state, data) {
    state.projects.node.parents = data
  },

  SET_DELTA_TREES (state, data) {
    state.projects.delta.trees = data
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
