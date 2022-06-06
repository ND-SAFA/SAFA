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
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var WarningModule = /** @class */ (function (_super) {
    __extends(WarningModule, _super);
    /**
     * This module defines the state of warnings generated for
     * artifacts and traces in this version.
     */
    function WarningModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * A collection of warnings keyed by the associated artifact.
         */
        _this.artifactWarnings = {};
        return _this;
    }
    /**
     * Sets the current collection of artifact warnings.
     *
     * @param warnings - A new collection of project warnings.
     */
    WarningModule.prototype.setArtifactWarnings = function (warnings) {
        this.SET_ARTIFACT_WARNINGS(warnings);
    };
    /**
     * Sets the current collection of artifact warnings.
     *
     * @param warnings - A new collection of project warnings.
     */
    WarningModule.prototype.SET_ARTIFACT_WARNINGS = function (warnings) {
        this.artifactWarnings = warnings;
    };
    Object.defineProperty(WarningModule.prototype, "getArtifactWarnings", {
        /**
         * @return The current artifact warnings.
         */
        get: function () {
            return this.artifactWarnings;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(WarningModule.prototype, "getWarningsByArtifactNames", {
        /**
         * @return Warnings associated with artifacts of given names.
         */
        get: function () {
            var _this = this;
            return function (names) {
                return names
                    .map(function (name) { return _this.artifactWarnings[name] || []; })
                    .reduce(function (acc, cur) { return __spreadArrays(acc, cur); }, []);
            };
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], WarningModule.prototype, "setArtifactWarnings");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], WarningModule.prototype, "SET_ARTIFACT_WARNINGS");
    WarningModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "warning" })
        /**
         * This module defines the state of warnings generated for
         * artifacts and traces in this version.
         */
    ], WarningModule);
    return WarningModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = WarningModule;
