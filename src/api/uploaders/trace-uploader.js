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
exports.__esModule = true;
exports.createTraceUploader = void 0;
var api_1 = require("@/api");
var util_1 = require("@/util");
var DEFAULT_IS_GENERATED = false;
/**
 * Creates a trace file uploader.
 */
function createTraceUploader() {
    return {
        panels: [],
        createNewPanel: createNewPanel
    };
}
exports.createTraceUploader = createTraceUploader;
/**
 * Creates a new uploader panel.
 *
 * @param traceLink - The like to create the panel for.
 */
function createNewPanel(traceLink) {
    var emptyArtifactFile = createTraceFile(traceLink);
    return {
        title: util_1.extractTraceId(traceLink),
        entityNames: [],
        projectFile: emptyArtifactFile,
        getIsValid: function () {
            return isArtifactPanelValid(this);
        },
        clearPanel: function () {
            return clearPanel(this);
        },
        parseFile: function (artifactMap, file) {
            return createParsedArtifactFile(artifactMap, this, file);
        },
        generateTraceLinks: function (artifactMap) {
            return generateTraceLinks(artifactMap, this);
        }
    };
}
/**
 * Generates all trace links between artifacts.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param panel - The trace panel to generate for.
 */
function generateTraceLinks(artifactMap, panel) {
    var sourceType = panel.projectFile.sourceId;
    var targetType = panel.projectFile.targetId;
    var artifacts = Object.values(artifactMap);
    var sourceArtifacts = artifacts.filter(function (a) { return a.type === sourceType; });
    var targetArtifacts = artifacts.filter(function (a) { return a.type === targetType; });
    return api_1.createGeneratedLinks(sourceArtifacts, targetArtifacts).then(function (traceLinks) {
        panel.projectFile.traces = traceLinks;
        panel.entityNames = traceLinks.map(util_1.extractTraceId);
    });
}
/**
 * Creates a new trace file.
 *
 * @param traceLink - The trace link in this file.
 */
function createTraceFile(traceLink) {
    return {
        sourceId: traceLink.sourceId,
        targetId: traceLink.targetId,
        isGenerated: DEFAULT_IS_GENERATED,
        isValid: false,
        errors: [],
        traces: []
    };
}
/**
 * Returns whether the panel is valid.
 *
 * @param panel - The panel to check.
 * @return Whether it is valid.
 */
function isArtifactPanelValid(panel) {
    return (panel.projectFile.file !== undefined &&
        panel.projectFile.errors.length === 0);
}
/**
 * Clears the panel.
 *
 * @param panel - The panel to clear.
 */
function clearPanel(panel) {
    panel.projectFile = __assign(__assign({}, panel.projectFile), { file: undefined, traces: [], errors: [] });
    panel.entityNames = [];
}
/**
 * Parses the uploaded trace links.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param panel - The trace panel.
 * @param file - The file to parse.
 */
function createParsedArtifactFile(artifactMap, panel, file) {
    return api_1.parseTraceFile(file).then(function (res) {
        var traces = res.traces, errors = res.errors;
        var validTraces = [];
        traces.forEach(function (link) {
            var error = getTraceError(panel.projectFile, artifactMap, link);
            if (error === undefined) {
                validTraces.push(link);
            }
            else {
                errors.push(error);
            }
        });
        panel.projectFile.traces = validTraces;
        panel.projectFile.errors = errors;
        panel.projectFile.file = file;
        panel.entityNames = traces.map(util_1.extractTraceId);
    });
}
/**
 * Returns any errors for the given trace link.
 *
 * @param traceFile - The trace file.
 * @param artifactMap - A collection of all artifacts.
 * @param traceLink - The trace to check.
 * @return The error message, if there is one.
 */
function getTraceError(traceFile, artifactMap, traceLink) {
    var sourceName = traceLink.sourceName, targetName = traceLink.targetName;
    if (!(sourceName in artifactMap)) {
        return "Artifact " + sourceName + " does not exist.";
    }
    else if (!(targetName in artifactMap)) {
        return "Artifact " + targetName + " does not exist.";
    }
    else {
        var sourceArtifact = artifactMap[sourceName];
        var targetArtifact = artifactMap[targetName];
        if (sourceArtifact.type !== traceFile.sourceId) {
            return sourceArtifact.name + " is not of type " + traceFile.sourceId + ".";
        }
        if (targetArtifact.type !== traceFile.targetId) {
            return targetArtifact.name + " is not of type " + traceFile.targetId + ".";
        }
    }
}
