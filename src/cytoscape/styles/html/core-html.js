"use strict";
exports.__esModule = true;
exports.htmlContainer = exports.htmlBody = exports.htmlSubheader = exports.htmlHeader = void 0;
var util_1 = require("@/util");
/**
 * Creates the HTML for representing a node's header.
 *
 * @param title - The title to render.
 *
 * @return stringified HTML for the node.
 */
function htmlHeader(title) {
    return "\n    <strong class=\"artifact-header text-body-1\" style=\"height: 28px\">\n      " + util_1.capitalize(title) + "\n    </strong>\n  ";
}
exports.htmlHeader = htmlHeader;
/**
 * Creates the HTML for representing an artifact's subheader.
 *
 * @param subtitle - The subtitle to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSubheader(subtitle) {
    return "\n    <span class=\"artifact-sub-header text-body-1\" style=\"height: 28px\">\n      " + subtitle + "\n    </span>\n  ";
}
exports.htmlSubheader = htmlSubheader;
/**
 * Creates the HTML for representing an artifact's body.
 *
 * @param body - The text body to render.
 * @param truncateLength - The max body length.
 * @param height - The height in pixes of the container.
 * @param width - The width in pixes of the container.
 *
 * @return stringified HTML for the node.
 */
function htmlBody(body, truncateLength, width, height) {
    var nodeWidth = width ? "width: " + width + "px;" : "";
    var nodeHeight = width ? "height: " + height + "px;" : "";
    body =
        body.length > truncateLength ? body.slice(0, truncateLength) + "..." : body;
    return "\n    <span class=\"text-body-2 artifact-body\" style=\"" + nodeWidth + nodeHeight + "\">\n      " + body + "\n    </span>\n  ";
}
exports.htmlBody = htmlBody;
/**
 * Creates the HTML for representing an artifact.
 *
 * @param elements - The elements to render within the container.
 * @param height - The height in pixes of the container.
 * @param width - The width in pixes of the container.
 * @param opacity - The opacity of the container.
 * @param color - The background color of the container.
 *
 * @return stringified HTML for the node.
 */
function htmlContainer(elements, _a) {
    var _b = _a === void 0 ? {} : _a, width = _b.width, height = _b.height, opacity = _b.opacity, color = _b.color;
    var backgroundColor = color ? "background-color: " + color + ";" : "";
    var visibility = opacity !== undefined ? "opacity: " + opacity + ";" : "";
    var nodeWidth = width ? "width: " + width + "px;" : "";
    var nodeHeight = height ? "height: " + height + "px;" : "";
    var classes = width && height
        ? "artifact-container artifact-border"
        : "artifact-container";
    return "\n    <div \n      class=\"" + classes + "\"\n      style=\"" + nodeWidth + nodeHeight + backgroundColor + visibility + "\"\n    >\n      " + elements.join("\n") + "\n    </div>\n  ";
}
exports.htmlContainer = htmlContainer;
