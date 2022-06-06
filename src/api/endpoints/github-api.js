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
exports.getGitHubRepositories = exports.getGitHubInstallations = exports.getGitHubRefreshToken = exports.getGitHubToken = exports.authorizeGitHub = void 0;
/**
 * The formatted scopes of jira permissions being requested.
 */
var scopes = encodeURI(["repo"].join(","));
/**
 * Runs a fetch call to the GitHub API.
 *
 * @param args - The fetch parameters to use.
 * @return The returned data.
 */
function fetchGitHub() {
    var args = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        args[_i] = arguments[_i];
    }
    return __awaiter(this, void 0, void 0, function () {
        var response, resJson;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch.apply(void 0, args)];
                case 1:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 2:
                    resJson = (_a.sent());
                    if (!response.ok) {
                        throw Error("Unable to connect to GitHub.");
                    }
                    else {
                        return [2 /*return*/, resJson];
                    }
                    return [2 /*return*/];
            }
        });
    });
}
/**
 * Runs a fetch call to the GitHub API using form data and returning params.
 *
 * @param data - The data to include in the body.
 * @param args - The fetch parameters to use.
 * @return The returned data.
 */
function fetchGitHubForm(data) {
    var args = [];
    for (var _i = 1; _i < arguments.length; _i++) {
        args[_i - 1] = arguments[_i];
    }
    return __awaiter(this, void 0, void 0, function () {
        var body, res, params, _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    body = new FormData();
                    Object.entries(data).forEach(function (_a) {
                        var key = _a[0], val = _a[1];
                        return body.append(key, val);
                    });
                    return [4 /*yield*/, fetch(args[0], __assign(__assign({}, args[1]), { body: body }))];
                case 1:
                    res = _b.sent();
                    _a = URLSearchParams.bind;
                    return [4 /*yield*/, res.text()];
                case 2:
                    params = new (_a.apply(URLSearchParams, [void 0, _b.sent()]))();
                    if (params.get("error")) {
                        throw new Error(params.get("error_description") || "Unable to connect to GitHub.");
                    }
                    return [2 /*return*/, params];
            }
        });
    });
}
/**
 * Opens an external link to authorize GitHub.
 */
function authorizeGitHub() {
    window.open("https://github.com/login/oauth/authorize?" +
        ("client_id=" + process.env.VUE_APP_GITHUB_CLIENT_ID + "&") +
        ("redirect_uri=" + process.env.VUE_APP_GITHUB_REDIRECT_LINK + "&") +
        ("scopes=" + scopes));
}
exports.authorizeGitHub = authorizeGitHub;
/**
 * Exchanges a GitHub access code for an API token.
 *
 * @param accessCode - The access code received from authorizing GitHub.
 * @return The GitHub access token.
 */
function getGitHubToken(accessCode) {
    return __awaiter(this, void 0, void 0, function () {
        var params;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetchGitHubForm({
                        code: accessCode,
                        client_id: process.env.VUE_APP_GITHUB_CLIENT_ID || "",
                        client_secret: process.env.VUE_APP_GITHUB_CLIENT_SECRET || "",
                        redirect_uri: process.env.VUE_APP_GITHUB_REDIRECT_LINK || ""
                    }, "https://github.com/login/oauth/access_token", {
                        method: "POST"
                    })];
                case 1:
                    params = _a.sent();
                    return [2 /*return*/, {
                            accessToken: params.get("access_token") || "",
                            refreshToken: params.get("refresh_token") || ""
                        }];
            }
        });
    });
}
exports.getGitHubToken = getGitHubToken;
/**
 * Exchanges a GitHub refresh token for an API token.
 *
 * @param refreshToken - The refresh token received from GitHub.
 * @return The GitHub access token.
 */
function getGitHubRefreshToken(refreshToken) {
    return __awaiter(this, void 0, void 0, function () {
        var params;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetchGitHubForm({
                        grant_type: "refresh_token",
                        refresh_token: refreshToken,
                        client_id: process.env.VUE_APP_GITHUB_CLIENT_ID || "",
                        client_secret: process.env.VUE_APP_GITHUB_CLIENT_SECRET || ""
                    }, "https://github.com/login/oauth/access_token", {
                        method: "POST"
                    })];
                case 1:
                    params = _a.sent();
                    return [2 /*return*/, {
                            accessToken: params.get("access_token") || "",
                            refreshToken: params.get("refresh_token") || ""
                        }];
            }
        });
    });
}
exports.getGitHubRefreshToken = getGitHubRefreshToken;
/**
 * Exchanges a GitHub access code for the list of installations associated with the given user.
 *
 * @param accessToken - The access token received from authorizing GitHub.
 * @return The GitHub organizations for this user.
 */
function getGitHubInstallations(accessToken) {
    return __awaiter(this, void 0, void 0, function () {
        var items;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetchGitHub("https://api.github.com/user/installations", {
                        method: "GET",
                        headers: {
                            Accept: "application/vnd.github.v3+json",
                            Authorization: "token " + accessToken
                        }
                    })];
                case 1:
                    items = _a.sent();
                    return [2 /*return*/, items.installations];
            }
        });
    });
}
exports.getGitHubInstallations = getGitHubInstallations;
/**
 * Returns all GitHub projects for the given user and installation.
 *
 * @param accessToken - The access token received from authorizing GitHub.
 * @param installationId - The GitHub installation id to return projects for.
 * @return The GitHub organizations for this user.
 */
function getGitHubRepositories(accessToken, installationId) {
    return __awaiter(this, void 0, void 0, function () {
        var repositories;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetchGitHub("https://api.github.com/user/installations/" + installationId + "/repositories", {
                        method: "GET",
                        headers: {
                            Accept: "application/vnd.github.v3+json",
                            Authorization: "token " + accessToken
                        }
                    })];
                case 1:
                    repositories = (_a.sent()).repositories;
                    return [2 /*return*/, repositories];
            }
        });
    });
}
exports.getGitHubRepositories = getGitHubRepositories;
