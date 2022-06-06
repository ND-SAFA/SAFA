"use strict";
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
exports.handleAuthentication = exports.handleLogout = exports.handleLogin = void 0;
var util_1 = require("@/util");
var router_1 = require("@/router");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Attempts to log a user in.
 *
 * @param user - The user to log in.
 */
function handleLogin(user) {
    return __awaiter(this, void 0, void 0, function () {
        var session, goToPath, query;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.createLoginSession(user)];
                case 1:
                    session = _a.sent();
                    goToPath = router_1.getParam(router_1.QueryParams.LOGIN_PATH);
                    query = __assign({}, router_1.getParams());
                    delete query[router_1.QueryParams.LOGIN_PATH];
                    store_1.sessionModule.SET_SESSION(session);
                    if (!(typeof goToPath === "string" && goToPath !== router_1.Routes.ARTIFACT)) return [3 /*break*/, 3];
                    return [4 /*yield*/, router_1.navigateTo(goToPath, query)];
                case 2:
                    _a.sent();
                    return [3 /*break*/, 6];
                case 3: return [4 /*yield*/, router_1.navigateTo(router_1.Routes.ARTIFACT, query)];
                case 4:
                    _a.sent();
                    return [4 /*yield*/, api_1.handleLoadLastProject()];
                case 5:
                    _a.sent();
                    _a.label = 6;
                case 6: return [2 /*return*/];
            }
        });
    });
}
exports.handleLogin = handleLogin;
/**
 * Logs a user out.
 */
function handleLogout() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    store_1.sessionModule.SET_SESSION(util_1.createSession());
                    return [4 /*yield*/, router_1.navigateTo(router_1.Routes.LOGIN_ACCOUNT)];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, api_1.handleClearProject()];
                case 2:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleLogout = handleLogout;
/**
 * Verifies the stored authentication token, and loads the last project if routing to the artifact tree.
 * If the token does not, is expired, or is otherwise invalid, the user will be sent back to login.
 */
function handleAuthentication() {
    return __awaiter(this, void 0, void 0, function () {
        var isAuthorized, location_1, e_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 6, , 8]);
                    return [4 /*yield*/, store_1.sessionModule.hasAuthorization()];
                case 1:
                    isAuthorized = _a.sent();
                    location_1 = window.location.href;
                    if (!!isAuthorized) return [3 /*break*/, 3];
                    return [4 /*yield*/, handleLogout()];
                case 2:
                    _a.sent();
                    return [3 /*break*/, 5];
                case 3:
                    if (!(isAuthorized && location_1.includes(router_1.Routes.ARTIFACT))) return [3 /*break*/, 5];
                    return [4 /*yield*/, api_1.handleLoadLastProject()];
                case 4:
                    _a.sent();
                    _a.label = 5;
                case 5: return [3 /*break*/, 8];
                case 6:
                    e_1 = _a.sent();
                    return [4 /*yield*/, handleLogout()];
                case 7:
                    _a.sent();
                    return [3 /*break*/, 8];
                case 8: return [2 /*return*/];
            }
        });
    });
}
exports.handleAuthentication = handleAuthentication;
