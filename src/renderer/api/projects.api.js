import httpClient from './http-client'
import eventSource from './event-source'
import { addNode, addElement } from '../lib/cytoscape/serializers'

const RELATIVE_API_PATH = 'projects'

// /project/{projId}/parents/{node}
async function getProjectNodeParents (projId, nodeId, rootType) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/parents/${nodeId}/?rootType=${rootType}`)
  return response.json()
}

// /{projId}/trees/
async function getProjectNodes (projId, nodeType) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/nodes/?nodeType=${nodeType}`)
  const json = await response.json()
  return json.reduce(addNode, []).sort((a, b) => {
    return (/UAV-(\d*)/.exec(a.id)[1]) - (/UAV-(\d*)/.exec(b.id)[1])
  })
}

// /project/{projId}/nodes/warnings
async function getProjectNodesWarnings (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/nodes/warnings`)
  return response.json()
}

// /project/{projId}/trees/
async function getProjectHierarchyTree (projId, rootType) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/trees/?rootType=${rootType}`)
  const json = await response.json()
  return json.reduce(addElement, [])
}

// /projects/{projId}/trees/{treeId}
async function getProjectSafetyArtifactTree (projId, treeId, rootType) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/trees/${treeId}/?rootType=${rootType}`)
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

async function getLinkTypes (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/linktypes/`)
  const json = await response.json()
  // const response = '{ "success": true, "message": "get link types success", "data": {"UAV-2": ["UAV-3", "UAV-4"], "UAV-6": ["UAV-9", "UAV-8"]}}'
  // const json = JSON.parse(response)
  console.log(json)
  return json
}

async function fetchApproverData (projId) {
  // const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/getapproverdata/`)
  // const json = await response.json()
  const response = '{ "success": true, "message": "send approver success", "data": {"UAV-200": {"desc":"test", "links": [ {"target": "UAV-700", "score": 0.8, "approval": 1, "desc": "demo description" }]}, "UAV-400": { "desc": "test 2", "links": [{"target": "UAV-1000", "score": 0.5, "approval": 2, "desc": "demo description 2" }, {"target": "UAV-12000", "score": 0.2, "approval": 0, "desc": "another description" }]} } }'
  const json = JSON.parse(response)
  console.log(json)
  return json
}

async function saveApproverData (projId, encodedStr) {
  // const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/saveapproverdata/`, { method: 'POST', body: encodedStr })
  // const json = await response.json()
  const response = '{ "success": true, "message": "send approver success", "data": {"UAV-200": {desc: “test”, links: [ {"target": "UAV-300", "score": 0.5, "approval": "not vetted", “desc”: “Demo descr” }]}, "UAV-400": { "desc": “test 2”, "links": [{"target": "UAV-700", "score": 0.2, "approval": "not vetted", “desc”: “Descr 2” }, {"target": "UAV-500", "score": 0.2, "approval": "not vetted", “desc”: "different description" }]} } }'
  const json = JSON.parse(response)
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
async function getDeltaTrees (projId, treeId, versions, rootType) {
  const responses = await Promise.all(versions.map(version => httpClient(`${RELATIVE_API_PATH}/${projId}/trees/${treeId}/versions/${version}/?rootType=${rootType}`)))
  const results = await Promise.all(responses.map(response => response.json()))
  return results.map(json => json.reduce(addElement, []))
}

function syncProject (projId) {
  return eventSource(`${RELATIVE_API_PATH}/${projId}/pull/`)
}

export default {
  getProjectNodeParents,
  getProjectNodes,
  getProjectNodesWarnings,
  getProjectHierarchyTree,
  getProjectSafetyArtifactTree,
  getProjectVersions,
  postProjectVersion,
  postFlatfileData,
  fetchErrorLog,
  generateTraceLinks,
  getLinkTypes,
  fetchApproverData,
  saveApproverData,
  fetchGenerateLinksErrorLog,
  removeTraceLinks,
  clearProjectFiles,
  getDeltaTrees,
  syncProject
}
