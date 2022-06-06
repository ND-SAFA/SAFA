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
exports.createArtifactUploader = void 0;
var api_1 = require("@/api");
/**
 * Creates an artifact uploader.
 */
function createArtifactUploader() {
    return {
        panels: [],
        createNewPanel: createNewPanel
    };
}
exports.createArtifactUploader = createArtifactUploader;
/**
 * Creates a new uploader panel.
 *
 * @param artifactName - The title of the panel.
 */
function createNewPanel(artifactName) {
    var emptyArtifactFile = createArtifactFile(artifactName);
    return {
        title: artifactName,
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
        }
    };
}
/**
 * Creates a new artifact file.
 *
 * @param artifactType - The artifact type in this file.
 */
function createArtifactFile(artifactType) {
    return {
        type: artifactType,
        file: undefined,
        artifacts: [],
        errors: [],
        isValid: false
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
    panel.projectFile = __assign(__assign({}, panel.projectFile), { file: undefined, artifacts: [], errors: [] });
    panel.entityNames = [];
}
/**
 * Parses the uploaded artifacts.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param panel - The artifact panel.
 * @param file - The file to parse.
 */
function createParsedArtifactFile(artifactMap, panel, file) {
    return api_1.parseArtifactFile(panel.projectFile.type, file)
        .then(function (res) {
        var artifacts = res.artifacts, errors = res.errors;
        var validArtifacts = [];
        artifacts.forEach(function (artifact) {
            var error = getArtifactError(artifactMap, artifact);
            if (error === undefined) {
                validArtifacts.push(artifact);
                artifactMap[artifact.name] = artifact;
            }
            else {
                errors.push(error);
            }
        });
        panel.projectFile = __assign(__assign({}, panel.projectFile), { artifacts: validArtifacts, errors: errors,
            file: file });
        panel.entityNames = artifacts.map(function (a) { return a.name; });
    })["catch"](function () {
        panel.projectFile.isValid = false;
        panel.projectFile.errors = ["Unable to parse file"];
    });
}
/**
 * Returns any errors for the given artifact.
 *
 * @param artifactMap - A collection of all artifacts.
 * @param artifact - The artifact to check.
 * @return The error message, if there is one.
 */
function getArtifactError(artifactMap, artifact) {
    if (artifact.name in artifactMap) {
        return "Could not parse duplicate artifact: " + artifact.name;
    }
}
