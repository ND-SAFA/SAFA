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
var events_1 = require("@/cytoscape/events");
var tim_klay_settings_1 = require("./tim-klay-settings");
var graph_layout_1 = require("./graph-layout");
var cytoscape_1 = require("@/cytoscape");
/**
 * Defines the layout of the tim graph.
 */
var TimGraphLayout = /** @class */ (function (_super) {
    __extends(TimGraphLayout, _super);
    function TimGraphLayout() {
        return _super.call(this, {}, events_1.DefaultCytoEvents, tim_klay_settings_1.TimKlaySettings, [], [function () { return cytoscape_1.cyCenterNodes(cytoscape_1.timTreeCyPromise); }]) || this;
    }
    return TimGraphLayout;
}(graph_layout_1["default"]));
exports["default"] = TimGraphLayout;
