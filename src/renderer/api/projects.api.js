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
async function getProjectVersions (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/versions/`)
  const json = await response.json()
  if (json.latest !== undefined && json.latest !== null) {
    return json
  }
  return {latest: 0}
}

// /projects/{projId}/versions/
// Save the current work as a new version
async function postProjectVersion (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/versions/`, { method: 'POST' })
  const json = await response.json()
  if (json.version !== undefined && json.version !== null) {
    return {latest: json.version}
  }
  return {latest: 0}
}

// /projects/{projId}/trees/{treeId}/versions/{version}
async function getDeltaTrees (projId, treeId, versions) {
  const responses = await Promise.all(versions.map(version => httpClient(`${RELATIVE_API_PATH}/${projId}/trees/${treeId}/versions/${version}`)))
  const results = await Promise.all(responses.map(response => response.json()))
  return results.map(json => json.reduce(addElement, []))
}

export default {
  getProjectNodeParents,
  getProjectHazards,
  getProjectHazardsWarnings,
  getProjectHazardTree,
  getProjectSafetyArtifactTree,
  getProjectVersions,
  postProjectVersion,
  getDeltaTrees
}
