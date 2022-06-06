"use strict";
exports.__esModule = true;
exports.LocalStorageKeys = exports.ConfirmationType = exports.PanelType = void 0;
/**
 * Enumerates types of panels.
 */
var PanelType;
(function (PanelType) {
    PanelType[PanelType["left"] = 0] = "left";
    PanelType[PanelType["right"] = 1] = "right";
    PanelType[PanelType["artifactCreator"] = 2] = "artifactCreator";
    PanelType[PanelType["errorDisplay"] = 3] = "errorDisplay";
})(PanelType = exports.PanelType || (exports.PanelType = {}));
var ConfirmationType;
(function (ConfirmationType) {
    ConfirmationType["INFO"] = "info";
    ConfirmationType["CLEAR"] = "clear";
})(ConfirmationType = exports.ConfirmationType || (exports.ConfirmationType = {}));
/**
 * Enumerates keys used in local storage.
 */
var LocalStorageKeys;
(function (LocalStorageKeys) {
    LocalStorageKeys["JIRA_REFRESH_TOKEN"] = "jrt";
    LocalStorageKeys["JIRA_CLOUD_ID"] = "jci";
    LocalStorageKeys["GIT_HUB_REFRESH_TOKEN"] = "grt";
    LocalStorageKeys["GIT_HUB_INSTALLATION_ID"] = "gid";
})(LocalStorageKeys = exports.LocalStorageKeys || (exports.LocalStorageKeys = {}));
