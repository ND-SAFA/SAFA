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
var store_1 = require("@/store");
var cytoscape_1 = require("@/cytoscape");
var ViewportModule = /** @class */ (function (_super) {
    __extends(ViewportModule, _super);
    /**
     * THis module manages the viewport of the artifact graph.
     */
    function ViewportModule() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ViewportModule.prototype.viewArtifactSubtree = function (artifact) {
        return __awaiter(this, void 0, void 0, function () {
            var artifactsInSubtree;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        artifactsInSubtree = __spreadArrays(store_1.subtreeModule.getSubtreeByArtifactId(artifact.id), [
                            artifact.id,
                        ]);
                        store_1.artifactSelectionModule.selectArtifact(artifact.id);
                        return [4 /*yield*/, store_1.artifactSelectionModule.filterGraph({
                                type: "subtree",
                                artifactsInSubtree: artifactsInSubtree
                            })];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    ViewportModule.prototype.repositionSelectedSubtree = function () {
        return __awaiter(this, void 0, void 0, function () {
            var artifactsInSubTree;
            var _this = this;
            return __generator(this, function (_a) {
                artifactsInSubTree = store_1.artifactSelectionModule.getSelectedSubtreeIds;
                cytoscape_1.cyIfNotAnimated(function () { return _this.centerOnArtifacts(artifactsInSubTree); });
                return [2 /*return*/];
            });
        });
    };
    ViewportModule.prototype.setArtifactTreeLayout = function () {
        return __awaiter(this, void 0, void 0, function () {
            var layout, payload;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        layout = new cytoscape_1.ArtifactGraphLayout();
                        payload = { layout: layout, cyPromise: cytoscape_1.artifactTreeCyPromise };
                        return [4 /*yield*/, this.setGraphLayout(payload)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    ViewportModule.prototype.setTimTreeLayout = function () {
        return __awaiter(this, void 0, void 0, function () {
            var layout, payload;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        layout = new cytoscape_1.TimGraphLayout();
                        payload = { layout: layout, cyPromise: cytoscape_1.timTreeCyPromise };
                        return [4 /*yield*/, this.setGraphLayout(payload)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    ViewportModule.prototype.setGraphLayout = function (layoutPayload) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                store_1.appModule.onLoadStart();
                this.SET_LAYOUT(layoutPayload.layout);
                cytoscape_1.cyCreateLayout(layoutPayload);
                this.applyAutomove();
                setTimeout(function () {
                    store_1.appModule.onLoadEnd();
                    cytoscape_1.cyCenterNodes();
                    cytoscape_1.cyResetTim();
                }, 200);
                return [2 /*return*/];
            });
        });
    };
    /**
     * Moves the viewport such that top most parent is centered at default zoom.
     * @param cyPromise - A promise returning a cytoscape instance whose root
     * node is calculated relative to.
     */
    ViewportModule.prototype.centerOnRootNode = function (cyPromise) {
        var _this = this;
        if (cyPromise === void 0) { cyPromise = cytoscape_1.artifactTreeCyPromise; }
        cyPromise.then(function (cy) {
            cytoscape_1.getRootNode(cy).then(function (rootNode) {
                var _a;
                if (!rootNode)
                    return;
                _this.centerOnArtifacts([(_a = rootNode.data()) === null || _a === void 0 ? void 0 : _a.id]);
            });
        });
    };
    /**
     * Moves the viewport such that given set of artifacts is in the middle of the viewport.
     * If no artifacts are given, the entire collection of nodes is centered.
     * Request is ignored if current animation is in progress to center the same collection of artifacts.
     *
     * @param artifactIds - The artifacts whose average point will be centered.
     * @param cyPromise - A promise returning an instance of cytoscape.
     */
    ViewportModule.prototype.centerOnArtifacts = function (artifactIds, cyPromise) {
        var _this = this;
        if (cyPromise === void 0) { cyPromise = cytoscape_1.artifactTreeCyPromise; }
        cytoscape_1.cyCenterOnArtifacts(this.currentCenteringCollection, artifactIds, function (ids) { return _this.SET_CURRENT_COLLECTION(ids); }, cyPromise);
    };
    /**
     * Deselects all artifacts.
     */
    ViewportModule.prototype.deselectArtifacts = function () {
        this.SET_CURRENT_COLLECTION([]);
    };
    /**
     * Resets all automove events.
     */
    ViewportModule.prototype.applyAutomove = function () {
        if (this.currentLayout) {
            cytoscape_1.cyApplyAutomove(this.currentLayout);
        }
    };
    /**
     * Sets a new layout.
     *
     * @param layout - The new layout to set.
     */
    ViewportModule.prototype.SET_LAYOUT = function (layout) {
        this.layout = layout;
    };
    /**
     * Sets a new centered collection of artifacts.
     *
     * @param centeringCollection - The new collection to set.
     */
    ViewportModule.prototype.SET_CURRENT_COLLECTION = function (centeringCollection) {
        this.currentCenteringCollection = centeringCollection;
    };
    Object.defineProperty(ViewportModule.prototype, "getNodesInView", {
        /**
         * @return artifact ids of those in viewport.
         */
        get: function () {
            var subtree = store_1.artifactSelectionModule.getSelectedSubtreeIds;
            var ignoreTypes = store_1.artifactSelectionModule.getIgnoreTypes;
            return store_1.artifactModule.artifacts
                .filter(function (a) { return cytoscape_1.isInSubtree(subtree, a) && cytoscape_1.doesNotContainType(ignoreTypes, a); })
                .map(function (a) { return a.id; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ViewportModule.prototype, "currentCenteredNodes", {
        /**
         * @return The currently centered nodes.
         */
        get: function () {
            return this.currentCenteringCollection || [];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ViewportModule.prototype, "currentLayout", {
        /**
         * @return The current layout.
         */
        get: function () {
            return this.layout;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "viewArtifactSubtree");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "repositionSelectedSubtree");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "setArtifactTreeLayout");
    __decorate([
        vuex_module_decorators_1.Action({ rawError: true })
    ], ViewportModule.prototype, "setTimTreeLayout");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "setGraphLayout");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "centerOnRootNode");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "centerOnArtifacts");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "deselectArtifacts");
    __decorate([
        vuex_module_decorators_1.Action
    ], ViewportModule.prototype, "applyAutomove");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ViewportModule.prototype, "SET_LAYOUT");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ViewportModule.prototype, "SET_CURRENT_COLLECTION");
    ViewportModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "viewport" })
        /**
         * THis module manages the viewport of the artifact graph.
         */
    ], ViewportModule);
    return ViewportModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = ViewportModule;
