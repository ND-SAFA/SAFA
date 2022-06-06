"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.artifactTreeMenuItems = void 0;
var store_1 = require("@/store");
var cytoscape_1 = require("@/cytoscape");
var api_1 = require("@/api");
var fta_menu_options_1 = require("./fta-menu-options");
var safety_case_menu_option_1 = require("./safety-case-menu-option");
/**
 * List of menu items
 */
exports.artifactTreeMenuItems = [
    {
        id: "add-artifact",
        content: "Add Artifact",
        tooltipText: "Create new artifact",
        coreAsWell: true,
        onClickFunction: function () {
            if (store_1.projectModule.isProjectDefined) {
                store_1.artifactSelectionModule.clearSelections();
                store_1.appModule.openArtifactCreatorTo();
            }
            else {
                store_1.logModule.onWarning("Please select a project to create artifacts.");
            }
        },
        isVisible: function () { return true; }
    },
    {
        id: "add-link",
        content: "Add Link",
        tooltipText: "Create new trace link",
        coreAsWell: true,
        onClickFunction: function () {
            if (store_1.projectModule.isProjectDefined) {
                cytoscape_1.enableDrawMode();
            }
            else {
                store_1.logModule.onWarning("Please select a project to create trace links.");
            }
        }
    },
    {
        id: "view-artifact",
        content: "View Artifact",
        tooltipText: "View Artifact",
        selector: "node",
        coreAsWell: false,
        onClickFunction: function (event) {
            handleOnClick(event, function (artifact) {
                store_1.artifactSelectionModule.selectArtifact(artifact.id);
            });
        },
        isVisible: function (artifactData) {
            return artifactData !== undefined;
        }
    },
    {
        id: "edit-artifact",
        content: "Edit Artifact",
        tooltipText: "Edit Artifact",
        selector: "node",
        coreAsWell: false,
        onClickFunction: function (event) {
            var _this = this;
            handleOnClick(event, function (artifact) { return __awaiter(_this, void 0, void 0, function () {
                return __generator(this, function (_a) {
                    store_1.artifactSelectionModule.selectArtifact(artifact.id);
                    store_1.appModule.openArtifactCreatorTo();
                    return [2 /*return*/];
                });
            }); });
        },
        isVisible: function (artifactData) {
            return artifactData !== undefined;
        }
    },
    {
        id: "delete-artifact",
        content: "Delete Artifact",
        tooltipText: "Delete Artifact",
        selector: "node",
        coreAsWell: false,
        onClickFunction: function (event) {
            var _this = this;
            handleOnClick(event, function (artifact) { return __awaiter(_this, void 0, void 0, function () {
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, api_1.handleDeleteArtifact(artifact, {})];
                        case 1:
                            _a.sent();
                            return [2 /*return*/];
                    }
                });
            }); });
        },
        isVisible: function (artifactData) {
            return artifactData !== undefined;
        }
    },
    {
        id: "duplicate-artifact",
        content: "Duplicate Artifact",
        tooltipText: "Duplicate Artifact",
        selector: "node",
        coreAsWell: false,
        onClickFunction: function (event) {
            var _this = this;
            handleOnClick(event, function (artifact) { return __awaiter(_this, void 0, void 0, function () {
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, api_1.handleDuplicateArtifact(artifact, {})];
                        case 1:
                            _a.sent();
                            return [2 /*return*/];
                    }
                });
            }); });
        },
        isVisible: function (artifactData) {
            return artifactData !== undefined;
        }
    },
    {
        id: "highlight-artifact-subtree",
        content: "Highlight Subtree",
        tooltipText: "Highlight Subtree",
        selector: "node",
        coreAsWell: false,
        onClickFunction: function (event) {
            handleOnClick(event, store_1.viewportModule.viewArtifactSubtree);
        },
        isVisible: hasSubtree
    },
    {
        id: "hide-artifact-subtree",
        content: "Hide Subtree",
        tooltipText: "Hide all children.",
        selector: "node",
        onClickFunction: function (event) {
            return __awaiter(this, void 0, void 0, function () {
                var artifactId;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            artifactId = event.target.data().id;
                            return [4 /*yield*/, store_1.subtreeModule.hideSubtree(artifactId)];
                        case 1:
                            _a.sent();
                            return [2 /*return*/];
                    }
                });
            });
        },
        isVisible: hasSubtree
    },
    {
        id: "show-artifact-subtree",
        content: "Show Subtree",
        tooltipText: "Show all hidden children.",
        selector: "node",
        onClickFunction: function (event) {
            return __awaiter(this, void 0, void 0, function () {
                var artifactId;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            artifactId = event.target.data().id;
                            return [4 /*yield*/, store_1.subtreeModule.showSubtree(artifactId)];
                        case 1:
                            _a.sent();
                            return [2 /*return*/];
                    }
                });
            });
        },
        isVisible: function (artifactData) {
            if (artifactData !== undefined) {
                return store_1.subtreeModule.getCollapsedParentNodes.includes(artifactData.id);
            }
            return false;
        }
    },
    fta_menu_options_1.ftaMenuItem,
    safety_case_menu_option_1.safetyCaseMenuOption,
];
function hasSubtree(artifactData) {
    if (artifactData !== undefined) {
        return !store_1.subtreeModule.getCollapsedParentNodes.includes(artifactData.id);
    }
    return false;
}
/**
 * Handles an artifact on click event.
 * @param event - The event,
 * @param handler - The handler to call with the event's artifact.
 */
function handleOnClick(event, handler) {
    if (event.target !== null) {
        var artifactData = event.target.data();
        var artifact = store_1.artifactModule.getArtifactByName(artifactData.artifactName);
        handler(artifact);
    }
}
