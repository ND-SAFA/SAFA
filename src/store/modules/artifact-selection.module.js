"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
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
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var types_1 = require("@/types");
var store_1 = require("@/store");
var ArtifactSelectionModule = /** @class */ (function (_super) {
    __extends(ArtifactSelectionModule, _super);
    /**
     * This module defines the currently selected artifact and downstream artifacts associated with it.
     */
    function ArtifactSelectionModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The currently selected artifact.
         */
        _this.selectedArtifactId = "";
        /**
         * The currently selected subtree.
         */
        _this.selectedSubtreeIds = [];
        /**
         * The currently selected group of nodes.
         */
        _this.selectedGroupIds = [];
        /**
         * Types to ignore.
         */
        _this.ignoreTypes = [];
        return _this;
    }
    ArtifactSelectionModule.prototype.filterGraph = function (filterAction) {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = filterAction.type;
                        switch (_a) {
                            case "ignore": return [3 /*break*/, 1];
                            case "subtree": return [3 /*break*/, 2];
                        }
                        return [3 /*break*/, 4];
                    case 1:
                        switch (filterAction.action) {
                            case "add":
                                return [2 /*return*/, this.ADD_IGNORE_TYPE(filterAction.ignoreType)];
                            case "remove":
                                return [2 /*return*/, this.REMOVE_IGNORE_TYPE(filterAction.ignoreType)];
                        }
                        return [3 /*break*/, 4];
                    case 2:
                        this.SET_SELECTED_SUBTREE(filterAction.artifactsInSubtree);
                        return [4 /*yield*/, store_1.viewportModule.repositionSelectedSubtree()];
                    case 3:
                        _b.sent();
                        _b.label = 4;
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Sets the given artifact as selected.
     *
     * @param artifactId - The artifact to select.
     */
    ArtifactSelectionModule.prototype.selectArtifact = function (artifactId) {
        this.SELECT_ARTIFACT(artifactId);
        store_1.appModule.openPanel(types_1.PanelType.left);
        store_1.viewportModule.centerOnArtifacts([artifactId]);
    };
    /**
     * Adds the given artifact to the selected group.
     *
     * @param artifactId - The artifact to select.
     */
    ArtifactSelectionModule.prototype.addToSelectedGroup = function (artifactId) {
        this.SELECT_GROUP(__spreadArrays(this.selectedGroupIds, [artifactId]));
    };
    /**
     * Clears any selected artifact(s) in artifact tree.
     */
    ArtifactSelectionModule.prototype.clearSelections = function () {
        this.SET_SELECTED_SUBTREE([]);
        this.SELECT_GROUP([]);
        this.UNSELECT_ARTIFACT();
        store_1.appModule.closePanel(types_1.PanelType.left);
    };
    /**
     * Sets a subtree of artifacts as selected.
     *
     * @param artifactIds - The artifact subtree to select.
     */
    ArtifactSelectionModule.prototype.SET_SELECTED_SUBTREE = function (artifactIds) {
        this.selectedSubtreeIds = artifactIds;
    };
    /**
     * Adds an artifact type to ignore from selection.
     *
     * @param artifactType - The type to ignore.
     */
    ArtifactSelectionModule.prototype.ADD_IGNORE_TYPE = function (artifactType) {
        this.ignoreTypes.push(artifactType);
    };
    /**
     * Removes an ignored artifact type.
     *
     * @param artifactType - The type to stop ignoring.
     */
    ArtifactSelectionModule.prototype.REMOVE_IGNORE_TYPE = function (artifactType) {
        this.ignoreTypes = this.ignoreTypes.filter(function (type) { return type !== artifactType; });
    };
    /**
     * Sets the given artifact as selected.
     *
     * @param artifactId - The ID of the artifact to select.
     */
    ArtifactSelectionModule.prototype.SELECT_ARTIFACT = function (artifactId) {
        this.selectedArtifactId = artifactId;
    };
    /**
     * Sets the given artifacts as a selected group.
     *
     * @param artifactIds - The IDs of the group of artifacts to select.
     */
    ArtifactSelectionModule.prototype.SELECT_GROUP = function (artifactIds) {
        this.selectedGroupIds = artifactIds;
    };
    /**
     * Unselects any selected artifact and closes the left app panel.
     */
    ArtifactSelectionModule.prototype.UNSELECT_ARTIFACT = function () {
        this.selectedArtifactId = "";
    };
    Object.defineProperty(ArtifactSelectionModule.prototype, "getSelectedArtifactId", {
        /**
         * @return The currently selected artifact id.
         */
        get: function () {
            return this.selectedArtifactId;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactSelectionModule.prototype, "getSelectedGroupIds", {
        /**
         * @return The currently selected artifact id.
         */
        get: function () {
            return this.selectedGroupIds;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactSelectionModule.prototype, "isArtifactSelected", {
        /**
         * @return Whether there is a currently selected artifact.
         */
        get: function () {
            return this.selectedArtifactId !== "";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactSelectionModule.prototype, "getSelectedArtifact", {
        /**
         * @return The currently selected artifact.
         */
        get: function () {
            if (this.selectedArtifactId !== "") {
                try {
                    return store_1.artifactModule.getArtifactById(this.selectedArtifactId);
                }
                catch (e) {
                    store_1.logModule.onError(e);
                }
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactSelectionModule.prototype, "getSelectedSubtreeIds", {
        /**
         * @return The currently selected artifact subtree.
         */
        get: function () {
            return this.selectedSubtreeIds;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactSelectionModule.prototype, "getIgnoreTypes", {
        /**
         * @return The currently ignored artifact types.
         */
        get: function () {
            return this.ignoreTypes;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactSelectionModule.prototype, "isArtifactInSelectedGroup", {
        /**
         * @return Whether the given artifact id is selected or in the selected group.
         */
        get: function () {
            var _this = this;
            return function (id) {
                return (id === _this.selectedArtifactId || _this.selectedGroupIds.includes(id));
            };
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactSelectionModule.prototype, "filterGraph");
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactSelectionModule.prototype, "selectArtifact");
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactSelectionModule.prototype, "addToSelectedGroup");
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactSelectionModule.prototype, "clearSelections");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactSelectionModule.prototype, "SET_SELECTED_SUBTREE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactSelectionModule.prototype, "ADD_IGNORE_TYPE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactSelectionModule.prototype, "REMOVE_IGNORE_TYPE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactSelectionModule.prototype, "SELECT_ARTIFACT");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactSelectionModule.prototype, "SELECT_GROUP");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactSelectionModule.prototype, "UNSELECT_ARTIFACT");
    ArtifactSelectionModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "artifactSelection" })
        /**
         * This module defines the currently selected artifact and downstream artifacts associated with it.
         */
    ], ArtifactSelectionModule);
    return ArtifactSelectionModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = ArtifactSelectionModule;
