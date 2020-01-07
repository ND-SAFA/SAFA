// import httpClient from './http-client'
import CytoscapeBuilder from '../classes/cytoscape-builder'
import httpClient from './http-client'

const RELATIVE_API_PATH = 'projects'

// /{projId}/parents/{node}
async function getProjectNodeParents (projId, node) {
  return httpClient(`${RELATIVE_API_PATH}/${projId}/parents/${node}/`)
}

// /{projId}/trees/
async function getProjectHazards (projId) {
  const response = await httpClient(`${RELATIVE_API_PATH}/${projId}/hazards/`)
  const json = await response.json()
  return json.reduce(CytoscapeBuilder.addNode, []).sort((a, b) => {
    return (/UAV-(\d*)/.exec(a.id)[1]) - (/UAV-(\d*)/.exec(b.id)[1])
  })
}

export default {
  getProjectNodeParents,
  getProjectHazards
}
