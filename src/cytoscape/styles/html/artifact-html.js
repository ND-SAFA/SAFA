"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
exports.artifactHtml = void 0;
var types_1 = require("@/types");
var config_1 = require("@/cytoscape/styles/config");
var util_1 = require("@/util");
var core_html_1 = require("./core-html");
/**
 * Renders artifact html.
 */
exports.artifactHtml = {
    query: "node",
    halign: "center",
    valign: "center",
    halignBox: "center",
    valignBox: "center",
    tpl: function (data) {
        if (!(data === null || data === void 0 ? void 0 : data.artifactType))
            return "";
        if (data.safetyCaseType) {
            return htmlSafetyCase(data);
        }
        else if (data.logicType) {
            return htmlFTA(data);
        }
        else {
            return htmlArtifact(data);
        }
    }
};
/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlFTA(data) {
    return core_html_1.htmlContainer([core_html_1.htmlSubheader(data.logicType || "")], {
        opacity: data.opacity,
        color: util_1.getBackgroundColor(data.artifactDeltaState)
    });
}
/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlArtifact(data) {
    var _a;
    var hasFooter = !!(((_a = data.warnings) === null || _a === void 0 ? void 0 : _a.length) || data.hiddenChildren);
    var truncateLength = hasFooter ? 100 : 150;
    var isCode = data.artifactType.toLowerCase().includes("code");
    return core_html_1.htmlContainer([
        core_html_1.htmlHeader(data.artifactType),
        core_html_1.htmlSubheader(data.artifactName),
        core_html_1.htmlBody(isCode ? "" : data.body, truncateLength),
        htmlFooter(data),
        htmlStoplight(data),
    ], {
        width: config_1.ARTIFACT_WIDTH * 1.95,
        height: config_1.ARTIFACT_HEIGHT * 2.7,
        opacity: data.opacity,
        color: util_1.getBackgroundColor(data.artifactDeltaState)
    });
}
/**
 * Creates the HTML for representing an artifact node's warning and collapsed children.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlFooter(data) {
    var _a, _b, _c, _d, _e, _f, _g, _h;
    var displayChildren = !!data.hiddenChildren;
    var displayWarning = !!((_a = data.warnings) === null || _a === void 0 ? void 0 : _a.length);
    var message = ((_c = (_b = data.warnings) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c.ruleName) || "Warning";
    var warningCount = ((_d = data.warnings) === null || _d === void 0 ? void 0 : _d.length) || 0;
    if (displayChildren) {
        displayWarning || (displayWarning = !!((_e = data.childWarnings) === null || _e === void 0 ? void 0 : _e.length));
        message = ((_g = (_f = data.childWarnings) === null || _f === void 0 ? void 0 : _f[0]) === null || _g === void 0 ? void 0 : _g.ruleName) || message;
        warningCount += ((_h = data.childWarnings) === null || _h === void 0 ? void 0 : _h.length) || 0;
    }
    var warning = "\n    <div class=\"d-flex flex-grow-1 px-1 warning-text text-body-1\">\n      <span class=\"material-icons md-18 pr-1\">warning</span>\n      <span class=\"artifact-footer-text\">(" + warningCount + ") " + message + "</span>\n    </div>\n  ";
    var hiddenChildren = "\n    <div class=\"d-flex flex-grow-1 pr-1 text-body-1\">\n      <span class=\"material-icons md-18\">expand_more</span>\n      <span>\n        " + data.hiddenChildren + " " + (displayWarning ? "" : "Hidden") + "\n      </span>\n    </div>\n  ";
    return "\n    <div class=\"artifact-footer\">\n      " + (displayChildren ? hiddenChildren : "") + "\n      " + (displayWarning ? warning : "") + "\n    </div>\n  ";
}
/**
 * Creates the HTML for representing an artifact node's child delta states.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlStoplight(data) {
    var _a = data.childDeltaStates, childDeltaStates = _a === void 0 ? [] : _a;
    if (!childDeltaStates.length)
        return "";
    var renderAdded = childDeltaStates.includes(types_1.ArtifactDeltaState.ADDED);
    var renderRemoved = childDeltaStates.includes(types_1.ArtifactDeltaState.REMOVED);
    var renderMod = childDeltaStates.includes(types_1.ArtifactDeltaState.MODIFIED);
    var classes = data.safetyCaseType
        ? "d-flex artifact-sc-stoplight"
        : "d-flex artifact-stoplight";
    return "\n    <div class=\"" + classes + "\">\n      " + (renderAdded ? "<div class='artifact-added flex-grow-1'></div>" : "") + "\n      " + (renderRemoved ? "<div class='artifact-removed flex-grow-1'></div>" : "") + "\n      " + (renderMod ? "<div class='artifact-modified flex-grow-1'></div>" : "") + "\n    </div>\n  ";
}
// Safety case
/**
 * Creates the HTML for representing an artifact node in a graph.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSafetyCase(data) {
    var _a;
    var attrs = { opacity: data.opacity };
    var header = [
        core_html_1.htmlHeader(((_a = data.safetyCaseType) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || ""),
        htmlStoplight(data),
        htmlSafetyCaseDetails(data),
    ];
    switch (data.safetyCaseType) {
        case "GOAL":
        case "CONTEXT":
            return core_html_1.htmlContainer(__spreadArrays(header, [core_html_1.htmlBody(data.body, 100, 200, 70)]), attrs);
        case "SOLUTION":
            return core_html_1.htmlContainer(__spreadArrays(header, [core_html_1.htmlBody(data.body, 40, 140, 60)]), __assign(__assign({}, attrs), { width: 140 }));
        case "STRATEGY":
            return core_html_1.htmlContainer(__spreadArrays(header, [core_html_1.htmlBody(data.body, 80, 170, 70)]), attrs);
        default:
            return "";
    }
}
/**
 * Creates the HTML for representing an artifact node's warning and collapsed children.
 *
 * @param data - The artifact data to render.
 *
 * @return stringified HTML for the node.
 */
function htmlSafetyCaseDetails(data) {
    var _a, _b;
    var displayChildren = !!data.hiddenChildren;
    var displayWarning = !!((_a = data.warnings) === null || _a === void 0 ? void 0 : _a.length);
    if (displayChildren) {
        displayWarning || (displayWarning = !!((_b = data.childWarnings) === null || _b === void 0 ? void 0 : _b.length));
    }
    var warning = "\n    <div class=\"d-flex warning-text text-body-1\">\n      <span class=\"material-icons md-18\">warning</span>\n    </div>\n  ";
    var hiddenChildren = "\n    <div class=\"d-flex text-body-1 pr-1\">\n      <span class=\"material-icons md-18\">expand_more</span>\n      <span>\n        " + data.hiddenChildren + " " + (displayWarning ? "" : "Hidden") + "\n      </span>\n    </div>\n  ";
    return "\n    <div class=\"artifact-sc-details\">\n      <span class=\"text-body-1 flex-grow-1\">\n        " + data.artifactName + "\n      </span>\n      " + (displayChildren ? hiddenChildren : "") + "\n      " + (displayWarning ? warning : "") + "\n    </div>\n  ";
}
