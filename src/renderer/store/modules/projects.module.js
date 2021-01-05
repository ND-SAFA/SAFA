/*
*   store/modules/projects.module.js
*/

// import the api endpoints
import projects from '@/api/projects.api'

const TEMP_PROJ_ID = 'spwd.cse.nd.edu'

const state = {
  projects: {
    syncProgress: -1,
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
  },

  getSyncProgress (state) {
    return state.projects.syncProgress
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
      commit('SET_PROJECT_VERSIONS', response)
    } catch (e) {
      // TODO(Adam): handle the error here
    }
  },

  async uploadFlatfileData ({ commit }, encodedStr) {
    try {
      const response = await projects.postFlatfileData(TEMP_PROJ_ID, encodedStr)
      console.log(response)
      console.log('api success')
      return response
      // commit('UPLOAD_FILES', response)
    } catch (e) {
      console.log(e)
      console.log('failed to upload flatfile data')
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
      commit('SET_DELTA_TREES', response)
    } catch (e) {
      // TODO(Adam): handle error
    }
  },

  async syncProject ({ commit }) {
    const evtSource = projects.syncProject(TEMP_PROJ_ID)
    commit('SET_SYNC_PROGRESS', 0)
    return new Promise((resolve, reject) => {
      evtSource.addEventListener('update', (message) => {
        commit('SET_SYNC_PROGRESS', message.lastEventId)
        if (JSON.parse(message.data).complete) {
          evtSource.close()
          commit('SET_SYNC_PROGRESS', -1)
          resolve()
        }
      })
      evtSource.onerror = (e) => {
        commit('SET_SYNC_PROGRESS', -1)
        reject(e)
      }
    })
  },

  resetProject ({ commit }) {
    commit('RESET_PROJECT')
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
  },

  SET_SYNC_PROGRESS (state, data) {
    state.projects.syncProgress = data
  },

  RESET_PROJECT (state) {
    state.projects = {
      syncProgress: -1,
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
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
