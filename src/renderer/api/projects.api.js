import httpClient from './http-client'
import eventSource from './event-source'
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

async function postFlatfileData (projId, encodedStr) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/upload/`, { method: 'POST', body: encodedStr })
  const json = await response.json()
  console.log('response from api on front end: ')
  console.log(json)
  return json
}

async function fetchErrorLog (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/errorlog/`)
  const json = await response.json()
  console.log('response from api on front end: ')
  console.log(json)
  return json
}

async function generateTraceLinks (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/generate/`)
  const json = await response.json()
  console.log('response for generate trace links')
  console.log(json)
  return json
}

async function fetchGenerateLinksErrorLog (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/linkserrorlog/`)
  const json = await response.json()
  console.log('response for generate trace links')
  console.log(json)
  return json
}

async function removeTraceLinks (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/remove/`)
  const json = await response.json()
  return json
}

async function clearProjectFiles (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/clear/`)
  const json = await response.json()
  console.log('response from api for clear project files: ', json)
  return json
}

// /projects/{projId}/trees/{treeId}/versions/{version}
async function getDeltaTrees (projId, treeId, versions) {
  const responses = await Promise.all(versions.map(version => httpClient(`${RELATIVE_API_PATH}/${projId}/trees/${treeId}/versions/${version}`)))
  const results = await Promise.all(responses.map(response => response.json()))
  return results.map(json => json.reduce(addElement, []))
}

function syncProject (projId) {
  return eventSource(`${RELATIVE_API_PATH}/${projId}/pull/`)
}

export default {
  getProjectNodeParents,
  getProjectHazards,
  getProjectHazardsWarnings,
  getProjectHazardTree,
  getProjectSafetyArtifactTree,
  getProjectVersions,
  postProjectVersion,
  postFlatfileData,
  fetchErrorLog,
  generateTraceLinks,
  fetchGenerateLinksErrorLog,
  removeTraceLinks,
  clearProjectFiles,
  getDeltaTrees,
  syncProject
}
