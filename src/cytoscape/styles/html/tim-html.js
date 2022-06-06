"use strict";
exports.__esModule = true;
exports.timNodeHtml = void 0;
var cytoscape_1 = require("@/cytoscape");
var core_html_1 = require("@/cytoscape/styles/html/core-html");
/**
 * Defines tim node html.
 */
exports.timNodeHtml = {
    query: "node",
    halign: "center",
    valign: "center",
    halignBox: "center",
    valignBox: "center",
    tpl: function (data) {
        if (!data)
            return "";
        return core_html_1.htmlContainer([
            "<span class=\"text-h6 artifact-header\" style=\"white-space: normal\">" + data.id + "</span>",
            "<span class=\"text-center text-body-1\" >" + data.count + "</span>",
        ], { width: cytoscape_1.TIM_NODE_WIDTH, height: cytoscape_1.TIM_NODE_HEIGHT });
    }
};
