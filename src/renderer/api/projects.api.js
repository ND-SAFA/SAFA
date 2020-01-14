import CytoscapeSAFABuilder from '../lib/cytoscape/prototypes'
import httpClient from './http-client'

const RELATIVE_API_PATH = 'projects'

// /project/{projId}/parents/{node}
async function getProjectNodeParents (projId, node) {
  return httpClient(`${RELATIVE_API_PATH}/${projId}/parents/${node}/`)
}

// /{projId}/trees/
async function getProjectHazards (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/hazards/`)
  const json = await response.json()
  return json.reduce(CytoscapeSAFABuilder.addNode, []).sort((a, b) => {
    return (/UAV-(\d*)/.exec(a.id)[1]) - (/UAV-(\d*)/.exec(b.id)[1])
  })
}

// /project/{projId}/trees/
async function getProjectHazardTree (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/trees/`)
  const json = await response.json()
  return json.reduce(CytoscapeSAFABuilder.addElement, [])
}

export default {
  getProjectNodeParents,
  getProjectHazards,
  getProjectHazardTree
}
