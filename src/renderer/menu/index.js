import { remote, Menu } from 'electron'
import Template from './template'

const _MENU = remote ? remote.Menu : Menu

export default class AppMenu {
  static __template = new Template(
    {
      label: 'File',
      id: 'file',
      submenu: [
        {
          id: 'open_fta',
          label: 'Open FTA File',
          accelerator: 'CommandOrControl+O'
        }
      ]
    },
    {
      label: 'View',
      id: 'view',
      submenu: [
        {
          id: 'refresh',
          label: 'Refresh',
          accelerator: 'CommandOrControl+R'
        },
        {
          id: 'graph_zoom_in',
          label: 'Graph Zoom In',
          accelerator: 'CommandOrControl+='
        },
        {
          id: 'graph_zoom_out',
          label: 'Graph Zoom Out',
          accelerator: 'CommandOrControl+-'
        }
      ]
    },
    {
      label: 'Project',
      id: 'project',
      submenu: [
        {
          id: 'sync',
          label: 'Synchronize Data',
          accelerator: 'CommandOrControl+P'
        },
        {
          id: 'freeze',
          label: 'Freeze Version',
          accelerator: 'CommandOrControl+S'
        },
        { type: 'separator' },
        {
          id: 'upload',
          label: 'Upload Flatfiles',
          accelerator: 'CommandOrControl+Q'
        },
        {
          id: 'tim',
          label: 'Create a TIM',
          accelerator: 'CommandOrControl+T'
        },
        {
          id: 'clear',
          label: 'Clear Current Uploads'
        },
        { type: 'separator' },
        {
          id: 'generate',
          label: 'Generate Trace Links',
          accelerator: 'CommandOrControl+L'
        },
        {
          id: 'approve',
          label: 'Approve Trace Links',
          accelerator: 'CommandOrControl+A'
        },
        {
          id: 'remove',
          label: 'Clear Generated Trace Links'
        },
        { type: 'separator' },
        {
          id: 'help',
          label: 'More Info'
        }
      ]
    }
  )

  static findMenuItemById (id) {
    try {
      let [menuId, subMenuId] = id.split('.')
      let menuItem = AppMenu.__template.find(i => i.id === menuId)
      if (subMenuId) {
        menuItem = menuItem.submenu.find(i => i.id === subMenuId)
      }
      return menuItem
    } catch (e) {
      return {}
    }
  }

  static template (template) {
    if (template instanceof Array) {
      AppMenu.__template = template
    }
    return AppMenu.__template
  }

  static setApplicationMenu () {
    if (AppMenu.__template) {
      const menu = _MENU.buildFromTemplate(AppMenu.__template)
      _MENU.setApplicationMenu(menu)
    }
  }
}
