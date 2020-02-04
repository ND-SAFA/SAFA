const IS_MAC_OS = (process.platform === 'darwin')

export default class Template extends Array {
  constructor () {
    super(...Array.prototype.slice.call(arguments))

    if (IS_MAC_OS) {
      this.unshift({role: 'appMenu'})
    } else if (this.length > 0 && this[0].submenu) {
      this[0].submenu.push(...[{ type: 'separator' }, { role: 'quit' }])
    }
  }
}
