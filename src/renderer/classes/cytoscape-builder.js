import Vue from 'vue'
import uuid from 'uuid'

export default class CytoscapeBuilder {
  static addNode (acc, e) {
    console.log(e)
    if (e.classes.startsWith('node')) {
      let data = {
        name: '',
        description: '',
        href: '',
        isDelegated: false,
        status: ''
      }
      if (e.DATA) {
        data = JSON.parse(Buffer.from(e.DATA, 'base64'))
      }
      data.type = data.type ? `${data.type}${e.label}` : e.label
      data.id = e.id || uuid.v4()
      data.label = `<b>${e.label}</br></b><div class="default-node-header">${data.id}</div><span class="default-node-description">${Vue.truncate(data.name)}</span>`
      if (e.label === 'Package') {
        // Only retain the package name information from the ID
        const dotIndex = e.id.indexOf('.')
        const packageName = e.id.slice(dotIndex + 1)
        data.label = `<b><i class="fas fa-folder"></i> ${e.label}</b></br><span class="package-node-wrap">${Vue.truncate(packageName, 70)}</span>`
      } else if (e.label === 'Code') {
        const slashIndex = e.id.lastIndexOf('/')
        const fileName = e.id.slice(slashIndex + 1)
        data.label = `${Vue.truncate(fileName, 22)}`
      }
      if (e.modified) {
        data.modified = e.modified
      }
      if (e.warnings && e.warnings.length) {
        data.warnings = e.warnings
        e.classes += ' warning'
      }
      acc.push({
        classes: e.classes,
        label: e.label,
        id: data.id,
        data: data
      })
    }
    return acc
  }
}
