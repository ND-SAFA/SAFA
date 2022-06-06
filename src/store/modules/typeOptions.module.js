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
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var util_1 = require("@/util");
var TypeOptionsModule = /** @class */ (function (_super) {
    __extends(TypeOptionsModule, _super);
    /**
     * This module tracks the directions of links between artifacts that are
     * allowed, and the icons for each type.
     */
    function TypeOptionsModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * A mapping of the allowed directions of links between artifacts.
         */
        _this.artifactTypeDirections = {};
        /**
         * A list of all artifact types.
         */
        _this.allArtifactTypes = [];
        /**
         * A mapping of the icons for each artifact type.
         */
        _this.artifactTypeIcons = util_1.createDefaultTypeIcons([]);
        return _this;
    }
    /**
     * Clears all store data.
     */
    TypeOptionsModule.prototype.clearData = function () {
        this.SET_LINK_DIRECTIONS({});
        this.SET_TYPE_ICONS(util_1.createDefaultTypeIcons([]));
        this.SET_TYPES([]);
    };
    /**
     * Changes what directions of trace links between artifacts are allowed.
     */
    TypeOptionsModule.prototype.initializeTypeIcons = function (artifactTypes) {
        this.SET_TYPE_ICONS(util_1.createDefaultTypeIcons(artifactTypes));
        this.SET_TYPES(artifactTypes);
    };
    /**
     * Changes what directions of trace links between artifacts are allowed.
     */
    TypeOptionsModule.prototype.updateLinkDirections = function (_a) {
        var _b;
        var type = _a.type, allowedTypes = _a.allowedTypes;
        this.SET_LINK_DIRECTIONS(__assign(__assign({}, this.artifactTypeDirections), (_b = {}, _b[type] = allowedTypes, _b)));
    };
    /**
     * Changes what icons each artifact uses.
     */
    TypeOptionsModule.prototype.updateArtifactIcon = function (_a) {
        var _b;
        var type = _a.type, icon = _a.icon;
        this.SET_TYPE_ICONS(__assign(__assign({}, this.artifactTypeIcons), (_b = {}, _b[type] = icon, _b)));
    };
    /**
     * Sets a new collection of allowed directions between artifact types.
     *
     * @param artifactTypeDirections - Directions between artifact types to allow.
     */
    TypeOptionsModule.prototype.SET_LINK_DIRECTIONS = function (artifactTypeDirections) {
        this.artifactTypeDirections = artifactTypeDirections;
    };
    /**
     * Sets the artifact types.
     *
     * @param artifactTypes - The artifact types.
     */
    TypeOptionsModule.prototype.SET_TYPES = function (artifactTypes) {
        this.allArtifactTypes = artifactTypes;
    };
    /**
     * Sets a new collection of artifact type icons.
     *
     * @param artifactTypeIcons - The icons for each artifact type.
     */
    TypeOptionsModule.prototype.SET_TYPE_ICONS = function (artifactTypeIcons) {
        this.artifactTypeIcons = artifactTypeIcons;
    };
    Object.defineProperty(TypeOptionsModule.prototype, "linkDirections", {
        /**
         * @returns The allowed directions of traces between artifacts.
         */
        get: function () {
            return this.artifactTypeDirections;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TypeOptionsModule.prototype, "artifactTypes", {
        /**
         * @returns all types of artifacts.
         */
        get: function () {
            return Object.keys(this.linkDirections);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TypeOptionsModule.prototype, "isLinkAllowedByType", {
        /**
         * @returns A function for determining if the trace link is allowed based on the type of the nodes.
         */
        get: function () {
            var _this = this;
            return function (sourceType, targetType) {
                var _a;
                //TODO: Add custom logic for tracing safety cases or FTA nodes.
                return !((_a = _this.artifactTypeDirections[targetType]) === null || _a === void 0 ? void 0 : _a.includes(sourceType));
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TypeOptionsModule.prototype, "allArtifactTypeIcons", {
        /**
         * @returns All possible artifact type icons.
         */
        get: function () {
            return [
                "mdi-clipboard-text",
                "mdi-math-compass",
                "mdi-hazard-lights",
                "mdi-pine-tree-fire",
                "mdi-help",
            ];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TypeOptionsModule.prototype, "getArtifactTypeIcon", {
        /**
         * @returns The icon name for the given artifact type
         */
        get: function () {
            var _this = this;
            return function (type) {
                return _this.artifactTypeIcons[type] || _this.artifactTypeIcons["default"];
            };
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], TypeOptionsModule.prototype, "clearData");
    __decorate([
        vuex_module_decorators_1.Action
    ], TypeOptionsModule.prototype, "initializeTypeIcons");
    __decorate([
        vuex_module_decorators_1.Action
    ], TypeOptionsModule.prototype, "updateLinkDirections");
    __decorate([
        vuex_module_decorators_1.Action
    ], TypeOptionsModule.prototype, "updateArtifactIcon");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], TypeOptionsModule.prototype, "SET_LINK_DIRECTIONS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], TypeOptionsModule.prototype, "SET_TYPES");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], TypeOptionsModule.prototype, "SET_TYPE_ICONS");
    TypeOptionsModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "typeOptions" })
        /**
         * This module tracks the directions of links between artifacts that are
         * allowed, and the icons for each type.
         */
    ], TypeOptionsModule);
    return TypeOptionsModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = TypeOptionsModule;
