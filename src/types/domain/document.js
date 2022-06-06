"use strict";
exports.__esModule = true;
exports.ColumnDataType = exports.DocumentType = void 0;
/**
 * Enumerates the type of documents supported by SAFA.
 */
var DocumentType;
(function (DocumentType) {
    DocumentType["ARTIFACT_TREE"] = "ARTIFACT_TREE";
    DocumentType["FTA"] = "FTA";
    DocumentType["SAFETY_CASE"] = "SAFETY_CASE";
    DocumentType["FMEA"] = "FMEA";
    DocumentType["FMECA"] = "FMECA";
})(DocumentType = exports.DocumentType || (exports.DocumentType = {}));
/**
 * Enumerates the types of columns in a table document.
 */
var ColumnDataType;
(function (ColumnDataType) {
    ColumnDataType["FREE_TEXT"] = "FREE_TEXT";
    ColumnDataType["RELATION"] = "RELATION";
    ColumnDataType["SELECT"] = "SELECT";
})(ColumnDataType = exports.ColumnDataType || (exports.ColumnDataType = {}));
