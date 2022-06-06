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
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var types_1 = require("@/types");
var ProjectModule = /** @class */ (function (_super) {
    __extends(ProjectModule, _super);
    /**
     * This module defines state variables shared across the entire app.
     */
    function ProjectModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Whether the app is currently loading.
         */
        _this.isLoading = false;
        /**
         * Whether the left panel is open.
         */
        _this.isLeftOpen = false;
        /**
         * Whether the right panel is open.
         */
        _this.isRightOpen = false;
        /**
         * Whether the error display is open.
         */
        _this.isErrorDisplayOpen = false;
        /**
         * Whether currently in create trace link mode.
         */
        _this.isCreateLinkEnabled = false;
        /**
         * Whether the artifact creator is open.
         * If the value is set to a safety case or FTA node type, then the
         * artifact creator will open to that type set.
         */
        _this.isArtifactCreatorOpen = false;
        return _this;
    }
    /**
     * Sets the app to loading.
     */
    ProjectModule.prototype.onLoadStart = function () {
        this.SET_IS_LOADING(true);
    };
    /**
     * Sets the app to no longer loading.
     */
    ProjectModule.prototype.onLoadEnd = function () {
        this.SET_IS_LOADING(false);
    };
    /**
     * Closes the side panels.
     */
    ProjectModule.prototype.openErrorDisplay = function () {
        this.openPanel(types_1.PanelType.errorDisplay);
    };
    /**
     * Toggles whether the right panel is open.
     */
    ProjectModule.prototype.toggleRightPanel = function () {
        this.TOGGLE_PANEL_STATE(types_1.PanelType.right);
    };
    /**
     * Toggles whether the left panel is open.
     */
    ProjectModule.prototype.toggleLeftPanel = function () {
        this.TOGGLE_PANEL_STATE(types_1.PanelType.left);
    };
    /**
     * Closes the side panels.
     */
    ProjectModule.prototype.closeSidePanels = function () {
        this.closePanel(types_1.PanelType.left);
        this.closePanel(types_1.PanelType.right);
    };
    /**
     * Closes the side panels.
     */
    ProjectModule.prototype.closeCreator = function () {
        this.closePanel(types_1.PanelType.artifactCreator);
    };
    /**
     * Closes the side panels.
     */
    ProjectModule.prototype.closeErrorDisplay = function () {
        this.closePanel(types_1.PanelType.errorDisplay);
    };
    /**
     * If a project is selected, opens the given panel.
     *
     * @param panel - The type of panel.
     */
    ProjectModule.prototype.openPanel = function (panel) {
        this.SET_PANEL_STATE({
            type: panel,
            isOpen: true
        });
    };
    /**
     * Closes the given panel.
     *
     * @param panel - The type of panel.
     */
    ProjectModule.prototype.closePanel = function (panel) {
        this.SET_PANEL_STATE({
            type: panel,
            isOpen: false
        });
    };
    /**
     * Opens the artifact creator to a specific node type.
     *
     * @param type - The type of panel.
     */
    ProjectModule.prototype.openArtifactCreatorTo = function (type) {
        this.SET_ARTIFACT_CREATOR(type || true);
    };
    /**
     * Sets whether trace link draw mode is enabled.
     *
     * @param enabled - Whether to enable the draw mode.
     */
    ProjectModule.prototype.SET_CREATE_LINK_ENABLED = function (enabled) {
        this.isCreateLinkEnabled = enabled;
    };
    /**
     * Sets the current loading state.
     *
     * @param isLoading - Whether the app is loading.
     */
    ProjectModule.prototype.SET_IS_LOADING = function (isLoading) {
        this.isLoading = isLoading;
    };
    /**
     * Sets the artifact creator state.
     *
     * @param isOpenOrType - The state of the artifact creator.
     */
    ProjectModule.prototype.SET_ARTIFACT_CREATOR = function (isOpenOrType) {
        this.isArtifactCreatorOpen = isOpenOrType;
    };
    /**
     * Sets whether a panel is open or closed.
     *
     * @param panelState - The panel type and whether it should be open.
     */
    ProjectModule.prototype.SET_PANEL_STATE = function (panelState) {
        var isOpen = panelState.isOpen;
        switch (panelState.type) {
            case types_1.PanelType.left:
                this.isLeftOpen = isOpen;
                break;
            case types_1.PanelType.right:
                this.isRightOpen = isOpen;
                break;
            case types_1.PanelType.artifactCreator:
                this.isArtifactCreatorOpen = isOpen;
                break;
            case types_1.PanelType.errorDisplay:
                this.isErrorDisplayOpen = isOpen;
                break;
            default:
                throw Error("Unrecognized panel: " + panelState.type);
        }
    };
    /**
     * Toggles the open state of the given panel.
     *
     * @param panel - The panel type to toggle.
     */
    ProjectModule.prototype.TOGGLE_PANEL_STATE = function (panel) {
        switch (panel) {
            case types_1.PanelType.left:
                this.isLeftOpen = !this.isLeftOpen;
                break;
            case types_1.PanelType.right:
                this.isRightOpen = !this.isRightOpen;
                break;
            default:
                throw Error(panel + " cannot be toggled");
        }
    };
    Object.defineProperty(ProjectModule.prototype, "getIsLoading", {
        /**
         * @return Whether the app is currently loading.
         */
        get: function () {
            return this.isLoading;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "getIsLeftOpen", {
        /**
         * @return Whether the left panel is open.
         */
        get: function () {
            return this.isLeftOpen;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "getIsRightOpen", {
        /**
         * @return Whether the right panel is open.
         */
        get: function () {
            return this.isRightOpen;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "getIsArtifactCreatorOpen", {
        /**
         * @return Whether the artifact creator is open.
         */
        get: function () {
            return this.isArtifactCreatorOpen;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "getIsErrorDisplayOpen", {
        /**
         * @return Whether the error display is open.
         */
        get: function () {
            return this.isErrorDisplayOpen;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "getIsCreateLinkEnabled", {
        /**
         * @return Whether trace link draw mode is currently enabled.
         */
        get: function () {
            return this.isCreateLinkEnabled;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "onLoadStart");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "onLoadEnd");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "openErrorDisplay");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "toggleRightPanel");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "toggleLeftPanel");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "closeSidePanels");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "closeCreator");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "closeErrorDisplay");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "openPanel");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "closePanel");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "openArtifactCreatorTo");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_CREATE_LINK_ENABLED");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_IS_LOADING");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_ARTIFACT_CREATOR");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_PANEL_STATE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "TOGGLE_PANEL_STATE");
    ProjectModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "app" })
        /**
         * This module defines state variables shared across the entire app.
         */
    ], ProjectModule);
    return ProjectModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = ProjectModule;
