/*
*   store/modules/projects.module.js
*/

// import the api endpoints
import projects from '@/api/projects.api'

const TEMP_PROJ_ID = 'spwd.cse.nd.edu'

const state = {
  projects: {
    syncProgress: -1,
    generateProgress: -1,
    delta: {
      trees: []
    },
    versions: {
      latest: 0
    },
    nodes: [],
    nodeTree: [],
    safetyArtifactTree: [],
    node: {
      parents: []
    },
    uploadFiles: null
  }
}

const getters = {
  getNodes (state) {
    return state.projects.nodes
  },

  getHierarchyTree (state) {
    return state.projects.hierarchyTree
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
  },

  getGenerateProgress (state) {
    return state.projects.generateProgress
  },

  getUploadFiles (state) {
    return state.projects.uploadFiles
  }
}

const actions = {
  async fetchNodes ({ commit }, nodeType) {
    try {
      const response = await projects.getProjectNodes(TEMP_PROJ_ID, nodeType)
      // Fetch node warnings at the same time
      const warnings = await projects.getProjectNodesWarnings(TEMP_PROJ_ID)
      // Store warnings in corresponding node
      for (const node of response) {
        node.warnings = warnings[node.id]
      }
      commit('SET_NODES', response)
    } catch (error) {
      console.log(error)
      // TODO(Adam): handle the error here
    }
  },

  async fetchHierarchyTree ({ commit }, rootType) {
    try {
      const response = await projects.getProjectHierarchyTree(TEMP_PROJ_ID, rootType)
      commit('SET_HIERARCHY_TREE', response)
    } catch (error) {
    }
  },

  async fetchSafetyArtifactTree ({ commit }, payload) {
    const { treeId, rootType } = payload
    console.log(treeId, rootType)
    try {
      const response = await projects.getProjectSafetyArtifactTree(TEMP_PROJ_ID, treeId, rootType)
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

  async uploadFlatfileData ({ commit }, filesStr) {
    try {
      const response = await projects.postFlatfileData(TEMP_PROJ_ID, filesStr)
      console.log(response)
      console.log('api success')
      return response
    } catch (e) {
      return 'Could not receive response from API'
    }
  },

  async fetchProjectNodeParents ({ commit }, payload) {
    const { nodeId, rootType } = payload
    try {
      const response = await projects.getProjectNodeParents(TEMP_PROJ_ID, nodeId, rootType)
      commit('SET_NODE_PARENTS', response)
    } catch (error) {
      // TODO(Adam): handle the error here
    }
  },

  async fetchDeltaTrees ({ commit }, payload) {
    const { treeId, baseline, current, rootType } = payload
    try {
      const response = await projects.getDeltaTrees(TEMP_PROJ_ID, treeId, [baseline, current], rootType)
      commit('SET_DELTA_TREES', response)
    } catch (e) {
      // TODO(Adam): handle error
    }
  },

  async syncProject ({ commit }) {
    console.log('starting syncProject function in projects.module')
    const evtSource = projects.syncProject(TEMP_PROJ_ID)
    commit('SET_SYNC_PROGRESS', 0)
    return new Promise((resolve, reject) => {
      evtSource.addEventListener('update', (message) => {
        var obj = JSON.parse(message.data)
        commit('SET_SYNC_PROGRESS', message.lastEventId)
        if (obj.complete) {
          evtSource.close()
          commit('SET_SYNC_PROGRESS', -1)
          resolve(obj)
        }
      })
      evtSource.onerror = (e) => {
        commit('SET_SYNC_PROGRESS', -1)
        reject(e)
      }
    })
  },

  async fetchErrorLog ({ commit }) {
    console.log('fetching error log')
    try {
      const response = await projects.fetchErrorLog(TEMP_PROJ_ID)
      return response
    } catch (error) {
      console.log(error)
    }
  },

  async generateTraceLinks ({ commit }) {
    try {
      commit('SET_GENERATE_PROGRESS', -1)
      commit('SET_GENERATE_PROGRESS', 1)
      const response = await projects.generateTraceLinks(TEMP_PROJ_ID)
      commit('SET_GENERATE_PROGRESS', -1)
      return response
    } catch (error) {
      commit('SET_GENERATE_PROGRESS', -1)
      console.log(error)
    }
  },

  async getLinkTypes ({ commit }) {
    try {
      const response = await projects.getLinkTypes(TEMP_PROJ_ID)
      return response
    } catch (error) {
      console.log(error)
    }
  },

  async getApproverData ({ commit }) {
    try {
      const response = await projects.fetchApproverData(TEMP_PROJ_ID)
      return response
    } catch (error) {
      console.log(error)
    }
  },

  async saveApproverData ({ commit }) {
    try {
      const response = await projects.saveApproverData(TEMP_PROJ_ID)
      return response
    } catch (error) {
      console.log(error)
    }
  },

  async getGenerateLinksErrorLog ({ commit }) {
    try {
      const response = await projects.fetchGenerateLinksErrorLog(TEMP_PROJ_ID)
      return response
    } catch (error) {
      console.log(error)
    }
  },

  async removeTraceLinks ({ commit }) {
    try {
      const response = await projects.removeTraceLinks(TEMP_PROJ_ID)
      return response
    } catch (error) {
      console.log(error)
    }
  },

  async clearUploads ({ commit }) {
    const response = await projects.clearProjectFiles(TEMP_PROJ_ID)
    return response
  },

  resetProject ({ commit }) {
    commit('RESET_PROJECT')
  }
}

const mutations = {
  SET_NODES (state, data) {
    state.projects.nodes = data
  },

  SET_HIERARCHY_TREE (state, data) {
    state.projects.hierarchyTree = data
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

  SET_GENERATE_PROGRESS (state, data) {
    state.projects.generateProgress = data
  },

  UPLOAD_FILES (state, data) {
    state.projects.uploadFiles = data
  },

  RESET_PROJECT (state) {
    state.projects = {
      syncProgress: -1,
      generateProgress: -1,
      delta: {
        trees: []
      },
      versions: {
        latest: 0
      },
      nodes: [],
      hierarchyTree: [],
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
