"use strict";
exports.__esModule = true;
exports.deltaTypeOptions = exports.columnTypeOptions = exports.logicTypeOptions = exports.safetyCaseOptions = exports.isTableDocument = exports.documentTypeMap = exports.documentTypeOptions = exports.createEnumOption = void 0;
var types_1 = require("@/types");
var string_helper_1 = require("@/util/string-helper");
/**
 * Converts an enum value into a selectable option with a title case name.
 *
 * @param enumValue - The enum value in upper snake case to convert.
 * @param name - The name of the option, which will bne generated if not given.
 * @return The selectable option.
 */
function createEnumOption(enumValue, name) {
    return { id: enumValue, name: name || string_helper_1.enumToDisplay(enumValue) };
}
exports.createEnumOption = createEnumOption;
/**
 * Returns display names for each document type.
 *
 * @return The select option names and ids.
 */
function documentTypeOptions() {
    return [
        createEnumOption(types_1.DocumentType.ARTIFACT_TREE, "Default"),
        createEnumOption(types_1.DocumentType.FTA, "FTA"),
        createEnumOption(types_1.DocumentType.SAFETY_CASE),
        createEnumOption(types_1.DocumentType.FMEA, "FMEA"),
        createEnumOption(types_1.DocumentType.FMECA, "FMECA"),
    ];
}
exports.documentTypeOptions = documentTypeOptions;
/**
 * Returns the document types of artifacts that can be created on a given document.
 *
 * @return The select option names and ids.
 */
function documentTypeMap() {
    var _a;
    var options = documentTypeOptions();
    return _a = {},
        _a[types_1.DocumentType.ARTIFACT_TREE] = [options[0]],
        _a[types_1.DocumentType.FTA] = [options[0], options[1]],
        _a[types_1.DocumentType.SAFETY_CASE] = [options[0], options[2]],
        _a[types_1.DocumentType.FMEA] = [options[0], options[3]],
        _a[types_1.DocumentType.FMECA] = [options[0], options[4]],
        _a;
}
exports.documentTypeMap = documentTypeMap;
/**
 * Returns whether the given document represents a table.
 *
 * @param type - The current document type.
 * @return Whether the type is for a table.
 */
function isTableDocument(type) {
    var tableDocuments = [types_1.DocumentType.FMEA, types_1.DocumentType.FMECA];
    return tableDocuments.includes(type);
}
exports.isTableDocument = isTableDocument;
/**
 * Returns display names for each safety case type.
 *
 * @return The select option names and ids.
 */
function safetyCaseOptions() {
    return [
        createEnumOption(types_1.SafetyCaseType.CONTEXT),
        createEnumOption(types_1.SafetyCaseType.GOAL),
        createEnumOption(types_1.SafetyCaseType.STRATEGY),
        createEnumOption(types_1.SafetyCaseType.SOLUTION),
    ];
}
exports.safetyCaseOptions = safetyCaseOptions;
/**
 * Returns display names for each logic type.
 *
 * @return The select option names and ids.
 */
function logicTypeOptions() {
    return [createEnumOption(types_1.FTANodeType.AND), createEnumOption(types_1.FTANodeType.OR)];
}
exports.logicTypeOptions = logicTypeOptions;
/**
 * Returns display names for each column type.
 *
 * @return The select option names and ids.
 */
function columnTypeOptions() {
    return [
        createEnumOption(types_1.ColumnDataType.FREE_TEXT, "Text"),
        createEnumOption(types_1.ColumnDataType.RELATION),
        createEnumOption(types_1.ColumnDataType.SELECT),
    ];
}
exports.columnTypeOptions = columnTypeOptions;
/**
 * Returns display names for each column type.
 *
 * @return The select option names and ids.
 */
function deltaTypeOptions() {
    return [
        createEnumOption(types_1.ArtifactDeltaState.NO_CHANGE),
        createEnumOption(types_1.ArtifactDeltaState.ADDED),
        createEnumOption(types_1.ArtifactDeltaState.MODIFIED),
        createEnumOption(types_1.ArtifactDeltaState.REMOVED),
    ];
}
exports.deltaTypeOptions = deltaTypeOptions;
