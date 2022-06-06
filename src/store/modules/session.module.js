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
var vuex_module_decorators_1 = require("vuex-module-decorators");
var jwt_decode_1 = require("jwt-decode");
var store_1 = require("@/store");
var util_1 = require("@/util");
var SessionModule = /** @class */ (function (_super) {
    __extends(SessionModule, _super);
    /**
     * This module defines the state of the current user session.
     */
    function SessionModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The current active session, if one exists.
         */
        _this.session = util_1.createSession();
        return _this;
    }
    SessionModule.prototype.updateSession = function (session) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.SET_SESSION(__assign(__assign({}, this.session), session));
                return [2 /*return*/];
            });
        });
    };
    SessionModule.prototype.hasAuthorization = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                if (this.isTokenEmpty) {
                    return [2 /*return*/, false];
                }
                else if (this.isTokenExpired) {
                    store_1.logModule.onWarning("Your session has expired, please log back in.");
                    return [2 /*return*/, false];
                }
                return [2 /*return*/, true];
            });
        });
    };
    /**
     * Sets the current session.
     */
    SessionModule.prototype.SET_SESSION = function (session) {
        this.session = session;
    };
    Object.defineProperty(SessionModule.prototype, "getDoesSessionExist", {
        /**
         * @return Whether there is a current session.
         */
        get: function () {
            return this.session.token !== "";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SessionModule.prototype, "getToken", {
        /**
         * @return The current authorization token if one exists.
         * @throws If the token does not exist.
         */
        get: function () {
            var token = this.session.token;
            if (token === "") {
                throw Error("No authorization token exists in store.");
            }
            return token;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SessionModule.prototype, "authenticationToken", {
        /**
         * Returns the decoded authentication token is one exists.
         * @throws If the token does not exist.
         */
        get: function () {
            try {
                return jwt_decode_1["default"](this.getToken);
            }
            catch (e) {
                store_1.logModule.onDevError(e);
                return undefined;
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SessionModule.prototype, "userEmail", {
        /**
         * Returns the authenticated user, if one exists.
         * @throws If the token does not exist.
         */
        get: function () {
            var _a;
            return ((_a = this.authenticationToken) === null || _a === void 0 ? void 0 : _a.sub) || "";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SessionModule.prototype, "isTokenEmpty", {
        /**
         * @return Whether a valid Authorization token is stored in module
         */
        get: function () {
            return this.session.token === "";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SessionModule.prototype, "isTokenExpired", {
        /**
         * @returns Whether the current JWT token is empty or has passed its
         * expiration date.
         * @throws If the token does not exist.
         */
        get: function () {
            var _a;
            var expirationTime = (((_a = this.authenticationToken) === null || _a === void 0 ? void 0 : _a.exp) || 0) * 1000;
            return this.isTokenEmpty || Date.now() >= expirationTime;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], SessionModule.prototype, "updateSession");
    __decorate([
        vuex_module_decorators_1.Action({ rawError: true })
    ], SessionModule.prototype, "hasAuthorization");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SessionModule.prototype, "SET_SESSION");
    SessionModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "session" })
        /**
         * This module defines the state of the current user session.
         */
    ], SessionModule);
    return SessionModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = SessionModule;
