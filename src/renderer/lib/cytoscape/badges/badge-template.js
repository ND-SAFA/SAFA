import Tippy from 'tippy.js'

export default class BadgeTemplate {
  static PLACEMENT = {
    TOP: 'top',
    TOP_END: 'top-start',
    TOP_START: 'top-end',
    BOTTOM: 'bottom',
    BOTTOM_START: 'bottom-start',
    BOTTOM_END: 'bottom-end',
    LEFT: 'left',
    LEFT_START: 'left-start',
    LEFT_END: 'left-end',
    RIGHT: 'right',
    RIGHT_START: 'right-start',
    RIGHT_END: 'right-end'
  }

  static TRIGGER = {
    MOUSEENTER: 'mouseenter',
    FOCUS: 'focus',
    MANUAL: 'manual',
    CLICK: 'click'
  }

  static SIZE = {
    SMALL: 'small',
    LARGE: 'large'
  }

  constructor (opts) {
    this.trigger = opts.trigger
    this.placement = opts.placement
    this.hideOnClick = opts.hideOnClick
    this.sticky = opts.sticky
    this.offset = opts.offset
    this.showOnInit = opts.showOnInit
    this.theme = opts.theme
    this.animateFill = opts.animateFill
    this.zIndex = opts.zIndex
    this.ignoreAttributes = opts.ignoreAttributes
    this.size = opts.size
  }

  fabricateFor (node) {
    this.content = `${node.data('changeIndex')}`
    return new Tippy(node.popperRef(), this)
  }
}
