"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
exports.__esModule = true;
var plugins_1 = require("@/cytoscape/plugins");
var events_1 = require("@/cytoscape/events");
var hooks_1 = require("@/cytoscape/hooks");
var artifact_klay_settings_1 = require("./artifact-klay-settings");
var graph_layout_1 = require("./graph-layout");
/**
 * Defines the layout of the artifact graph.
 */
var ArtifactGraphLayout = /** @class */ (function (_super) {
    __extends(ArtifactGraphLayout, _super);
    function ArtifactGraphLayout() {
        return _super.call(this, plugins_1.ArtifactTreeAutoMoveHandlers, events_1.ArtifactTreeCytoEvents, artifact_klay_settings_1.ArtifactKlaySettings, hooks_1.DefaultPreLayoutHooks, hooks_1.DefaultPostLayoutHooks) || this;
    }
    return ArtifactGraphLayout;
}(graph_layout_1["default"]));
exports["default"] = ArtifactGraphLayout;
