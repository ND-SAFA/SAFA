"use strict";
exports.__esModule = true;
exports.DefaultPostLayoutHooks = exports.dynamicVisibilityHookForContextMenuItems = exports.centerViewOnNode = exports.applyCytoEvents = exports.applyAutoMoveEvents = exports.addAutoMoveToNode = void 0;
var types_1 = require("@/types");
var store_1 = require("@/store");
var cytoscape_1 = require("@/cytoscape");
var util_1 = require("@/util");
var plugins_1 = require("@/cytoscape/plugins");
/**
 * Adds auto-move handlers to a node, so that its child nodes are dragged along with it.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 * @param node - The node to add handlers for.
 */
function addAutoMoveToNode(cy, layout, node) {
    var rule = cy.automove({
        nodesMatching: node.successors("node"),
        reposition: types_1.AutoMoveReposition.DRAG,
        dragWith: node
    });
    var _loop_1 = function (eventDefinition) {
        node.on(eventDefinition.triggers.join(" "), function (event) {
            eventDefinition.action(node, rule, event);
        });
    };
    for (var _i = 0, _a = Object.values(layout.autoMoveHandlers); _i < _a.length; _i++) {
        var eventDefinition = _a[_i];
        _loop_1(eventDefinition);
    }
}
exports.addAutoMoveToNode = addAutoMoveToNode;
/**
 * Adds auto-move handlers to all nodes, so that their children nodes are dragged along with then.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 */
var applyAutoMoveEvents = function (cy, layout) {
    cy.automove("destroy");
    cy.nodes().forEach(function (node) { return addAutoMoveToNode(cy, layout, node); });
};
exports.applyAutoMoveEvents = applyAutoMoveEvents;
/**
 * Applies cytoscape event handlers in the layout.
 *
 * @param cy - The cy instance.
 * @param layout - The layout instance.
 */
var applyCytoEvents = function (cy, layout) {
    var _loop_2 = function (cytoEvent) {
        var eventName = cytoEvent.events.join(" ");
        var selector = cytoEvent.selector;
        var handler = function (event) { return cytoEvent.action(cy, event); };
        if (selector === undefined) {
            cy.on(eventName, handler);
        }
        else {
            cy.on(eventName, selector, handler);
        }
    };
    for (var _i = 0, _a = Object.values(layout.cytoEventHandlers); _i < _a.length; _i++) {
        var cytoEvent = _a[_i];
        _loop_2(cytoEvent);
    }
};
exports.applyCytoEvents = applyCytoEvents;
/**
 * Centers on the selected or root node of the graph.
 */
var centerViewOnNode = function () {
    var selectedArtifacts = store_1.artifactSelectionModule.getSelectedArtifactId;
    if (!selectedArtifacts) {
        cytoscape_1.cyZoomReset();
        cytoscape_1.cyCenterNodes();
    }
    else {
        store_1.viewportModule.centerOnArtifacts([selectedArtifacts]);
    }
};
exports.centerViewOnNode = centerViewOnNode;
var initDynamic = true;
/**
 * Attaches hook to every right click on the cytoscape instance enabling
 * the dynamic showing of context menu items through lambda `isVisible`.
 *
 * @param cy The cytoscape instance
 */
var dynamicVisibilityHookForContextMenuItems = function (cy) {
    if (!initDynamic)
        return;
    initDynamic = false;
    cy.on(types_1.CytoEvent.CXT_TAP, function (event) {
        var data = event.target.data();
        var artifactData = util_1.isArtifactData(data)
            ? data
            : undefined;
        var contextMenuInstance = cy.contextMenus("get");
        plugins_1.artifactTreeMenuItems.forEach(function (menuItem) {
            if (menuItem.coreAsWell ||
                (menuItem.isVisible !== undefined && menuItem.isVisible(artifactData))) {
                contextMenuInstance.showMenuItem(menuItem.id);
            }
            else {
                contextMenuInstance.hideMenuItem(menuItem.id);
            }
        });
    });
};
exports.dynamicVisibilityHookForContextMenuItems = dynamicVisibilityHookForContextMenuItems;
exports.DefaultPostLayoutHooks = [
    exports.centerViewOnNode,
    exports.applyAutoMoveEvents,
    exports.applyCytoEvents,
    exports.dynamicVisibilityHookForContextMenuItems,
];
