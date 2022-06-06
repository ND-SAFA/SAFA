"use strict";
exports.__esModule = true;
exports.VersionMessageType = exports.ProjectMessageType = void 0;
/**
 * Enumerates the type of notification messages that signal
 * that a project meta entity should be updated.
 */
var ProjectMessageType;
(function (ProjectMessageType) {
    ProjectMessageType["MEMBERS"] = "MEMBERS";
    ProjectMessageType["DOCUMENTS"] = "DOCUMENTS";
    ProjectMessageType["META"] = "META";
})(ProjectMessageType = exports.ProjectMessageType || (exports.ProjectMessageType = {}));
/**
 * Enumerates the types of notifications messages that trigger
 * updates of the versioned entities
 */
var VersionMessageType;
(function (VersionMessageType) {
    VersionMessageType["VERSION"] = "VERSION";
    VersionMessageType["ARTIFACTS"] = "ARTIFACTS";
    VersionMessageType["TRACES"] = "TRACES";
    VersionMessageType["WARNINGS"] = "WARNINGS";
})(VersionMessageType = exports.VersionMessageType || (exports.VersionMessageType = {}));
