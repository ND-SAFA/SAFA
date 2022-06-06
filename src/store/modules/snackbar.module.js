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
var types_1 = require("@/types");
var util_1 = require("@/util");
var SnackbarModule = /** @class */ (function (_super) {
    __extends(SnackbarModule, _super);
    /**
     * This module controls snackbar messages.
     */
    function SnackbarModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The current snackbar message.
         */
        _this.snackbarMessage = util_1.createSnackbarMessage();
        /**
         * Whether the confirmation modal is open.
         */
        _this.confirmationMessage = util_1.createConfirmDialogueMessage();
        /**
         * A list of dev messages.
         */
        _this.devMessages = [];
        return _this;
    }
    /**
     * Creates a snackbar error message with the given server error.
     *
     * @param error - The error encountered.
     */
    SnackbarModule.prototype.onServerError = function (error) {
        var _a = error || {}, _b = _a.message, message = _b === void 0 ? "An unexpected error occurred." : _b, _c = _a.errors, errors = _c === void 0 ? [] : _c;
        this.SET_MESSAGE({
            message: message,
            type: types_1.MessageType.ERROR,
            errors: errors
        });
    };
    /**
     * Creates a snackbar error message with the given message.
     *
     * @param message - The error message encountered.
     */
    SnackbarModule.prototype.onError = function (message) {
        this.SET_MESSAGE({ message: message, type: types_1.MessageType.ERROR, errors: [] });
    };
    /**
     * Creates a snackbar information message with the given message.
     *
     * @param message - The message to display.
     */
    SnackbarModule.prototype.onInfo = function (message) {
        this.SET_MESSAGE({ message: message, type: types_1.MessageType.INFO, errors: [] });
    };
    /**
     * Creates a snackbar warning message with the given message.
     *
     * @param message - The message to display.
     */
    SnackbarModule.prototype.onWarning = function (message) {
        this.SET_MESSAGE({ message: message, type: types_1.MessageType.WARNING, errors: [] });
    };
    /**
     * Creates a snackbar success message with the given message.
     *
     * @param message - The message to display.
     */
    SnackbarModule.prototype.onSuccess = function (message) {
        this.SET_MESSAGE({ message: message, type: types_1.MessageType.SUCCESS, errors: [] });
    };
    /**
     * Logs and prints message to the console.
     */
    SnackbarModule.prototype.onDevMessage = function (message) {
        console.log(message);
        this.ADD_DEV_MESSAGE("Info: " + message);
    };
    /**
     * Logs and prints warning to the console.
     */
    SnackbarModule.prototype.onDevWarning = function (message) {
        console.warn(message);
        this.ADD_DEV_MESSAGE("Warning: " + message);
    };
    /**
     * Logs and prints error to the console.
     */
    SnackbarModule.prototype.onDevError = function (message) {
        console.error(message);
        this.ADD_DEV_MESSAGE("Error: " + message);
    };
    /**
     * Sets the current snackbar message.
     *
     * @param message - The message to display.
     */
    SnackbarModule.prototype.ADD_DEV_MESSAGE = function (message) {
        this.devMessages = __spreadArrays(this.devMessages, [message]);
    };
    /**
     * Sets the current snackbar message.
     *
     * @param message - The message to display.
     */
    SnackbarModule.prototype.SET_MESSAGE = function (message) {
        this.snackbarMessage = message;
    };
    /**
     * Clears the current snackbar message.
     */
    SnackbarModule.prototype.CLEAR_MESSAGE = function () {
        this.snackbarMessage = {
            message: "",
            type: types_1.MessageType.CLEAR,
            errors: []
        };
    };
    /**
     * Sets a snackbar message that the current feature isn't implemented.
     */
    SnackbarModule.prototype.NOT_IMPLEMENTED_ERROR = function () {
        this.snackbarMessage = {
            message: "This feature is under construction",
            type: types_1.MessageType.WARNING,
            errors: []
        };
    };
    /**
     * Shows message in confirmation box to user, returns whether confirmed or not.
     *
     */
    SnackbarModule.prototype.SET_CONFIRMATION_MESSAGE = function (message) {
        this.confirmationMessage = message;
    };
    /**
     * Shows message in confirmation box to user, returns whether confirmed or not.
     *
     */
    SnackbarModule.prototype.CLEAR_CONFIRMATION_MESSAGE = function () {
        this.confirmationMessage = util_1.createConfirmDialogueMessage();
    };
    Object.defineProperty(SnackbarModule.prototype, "getMessage", {
        /**
         * @return The current snackbar message.
         */
        get: function () {
            return this.snackbarMessage;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SnackbarModule.prototype, "getConfirmationMessage", {
        /**
         * @return THe current confirmation message.
         */
        get: function () {
            return this.confirmationMessage;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onServerError");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onError");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onInfo");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onWarning");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onSuccess");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onDevMessage");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onDevWarning");
    __decorate([
        vuex_module_decorators_1.Action
    ], SnackbarModule.prototype, "onDevError");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SnackbarModule.prototype, "ADD_DEV_MESSAGE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SnackbarModule.prototype, "SET_MESSAGE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SnackbarModule.prototype, "CLEAR_MESSAGE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SnackbarModule.prototype, "NOT_IMPLEMENTED_ERROR");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SnackbarModule.prototype, "SET_CONFIRMATION_MESSAGE");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SnackbarModule.prototype, "CLEAR_CONFIRMATION_MESSAGE");
    SnackbarModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "snackbar" })
        /**
         * This module controls snackbar messages.
         */
    ], SnackbarModule);
    return SnackbarModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = SnackbarModule;
