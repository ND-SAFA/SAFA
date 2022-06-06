"use strict";
exports.__esModule = true;
exports.artifactTreeContextMenuOptions = void 0;
var types_1 = require("@/types");
var menu_options_1 = require("./menu-options");
/**
 * Defines the options on the artifact tree context menu.
 */
exports.artifactTreeContextMenuOptions = {
    // Customize event to bring up the context menu
    // Possible options https://js.cytoscape.org/#events/user-input-device-events
    evtType: types_1.CytoEvent.CXT_TAP,
    // List of initial menu items
    // A menu item must have either onClickFunction or submenu or both
    menuItems: menu_options_1.artifactTreeMenuItems,
    // css classes that menu items will have
    menuItemClasses: [],
    // css classes that context menu will have
    contextMenuClasses: [],
    submenuIndicator: {
        src: "assets/submenu-indicator-default.svg",
        width: 12,
        height: 12
    }
};
