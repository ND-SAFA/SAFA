"use strict";
exports.__esModule = true;
exports.isTracePanel = exports.isTraceFile = exports.isArtifactData = exports.isArtifact = exports.isModifiedArtifact = void 0;
/**
 * Returns whether the given artifact or delta is a modified artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is a modified artifact.
 */
function isModifiedArtifact(artifact) {
    var requiredFields = ["before", "after"];
    return containsFields(artifact, requiredFields);
}
exports.isModifiedArtifact = isModifiedArtifact;
/**
 * Returns whether the given artifact or delta is an artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is an artifact.
 */
function isArtifact(artifact) {
    var requiredFields = ["id", "summary", "body", "type"];
    return containsFields(artifact, requiredFields);
}
exports.isArtifact = isArtifact;
/**
 * Returns whether the given cytoscape data is an artifact.
 *
 * @param artifact - The artifact to check.
 * @return Whether this item is an artifact.
 */
function isArtifactData(artifact) {
    var requiredFields = [
        "body",
        "artifactName",
        "artifactType",
        "artifactDeltaState",
        "isSelected",
        "opacity",
    ];
    return containsFields(artifact, requiredFields);
}
exports.isArtifactData = isArtifactData;
/**
 * Returns whether an object contains certain fields.
 *
 * @param object - The object to check.
 * @param fields - The fields required to exist on the object.
 * @return Whether this object has all required fields.
 */
function containsFields(object, fields) {
    return fields
        .map(function (field) { return field in object; })
        .reduce(function (prev, curr) { return prev && curr; }, true);
}
/**
 * Determines whether this project file is a trace file.
 *
 * @param file - The project file to check.
 *
 * @return Whether this file is a trace file.
 */
function isTraceFile(file) {
    var requiredFields = ["sourceId", "targetId", "isGenerated", "traces"];
    return containsFields(file, requiredFields);
}
exports.isTraceFile = isTraceFile;
/**
 * Determines whether this panel is a trace panel.
 *
 * @param panel - The panel to check.
 *
 * @return Whether this panel is a trace panel.
 */
function isTracePanel(panel) {
    return isTraceFile(panel.projectFile);
}
exports.isTracePanel = isTracePanel;
