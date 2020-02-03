import httpClient from './http-client'
import { addNode, addElement } from '../lib/cytoscape/serializers'

const RELATIVE_API_PATH = 'projects'

// /project/{projId}/parents/{node}
async function getProjectNodeParents (projId, nodeId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/parents/${nodeId}/`)
  return response.json()
}

// /{projId}/trees/
async function getProjectHazards (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/hazards/`)
  const json = await response.json()
  return json.reduce(addNode, []).sort((a, b) => {
    return (/UAV-(\d*)/.exec(a.id)[1]) - (/UAV-(\d*)/.exec(b.id)[1])
  })
}

// /project/{projId}/hazards/warnings
async function getProjectHazardsWarnings (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/hazards/warnings`)
  return response.json()
}

// /project/{projId}/trees/
async function getProjectHazardTree (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/trees/`)
  const json = await response.json()
  return json.reduce(addElement, [])
}

// /projects/{projId}/trees/{treeId}
async function getProjectSafetyArtifactTree (projId, treeId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/trees/${treeId}/`)
  const json = await response.json()
  return json.reduce(addElement, [])
}

// /projects/{projId}/versions/
async function fetchProjectVersions (projId) {
  const response = await fetch(`${RELATIVE_API_PATH}/${projId}/versions/`)
  const json = await response.json()
  if (json.latest !== undefined && json.latest !== null) {
    return json.latest
  }
  return 0
}

export default {
  getProjectNodeParents,
  getProjectHazards,
  getProjectHazardsWarnings,
  getProjectHazardTree,
  getProjectSafetyArtifactTree,
  fetchProjectVersions
}
