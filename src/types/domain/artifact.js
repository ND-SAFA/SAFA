"use strict";
exports.__esModule = true;
exports.SafetyCaseType = exports.FTANodeType = void 0;
/**
 * Enumerates the types of FTA nodes.
 */
var FTANodeType;
(function (FTANodeType) {
    FTANodeType["OR"] = "OR";
    FTANodeType["AND"] = "AND";
})(FTANodeType = exports.FTANodeType || (exports.FTANodeType = {}));
/**
 * Enumerates the types of safety cases.
 */
var SafetyCaseType;
(function (SafetyCaseType) {
    SafetyCaseType["GOAL"] = "GOAL";
    SafetyCaseType["SOLUTION"] = "SOLUTION";
    SafetyCaseType["CONTEXT"] = "CONTEXT";
    SafetyCaseType["STRATEGY"] = "STRATEGY";
})(SafetyCaseType = exports.SafetyCaseType || (exports.SafetyCaseType = {}));
