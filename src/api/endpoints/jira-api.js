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
exports.createJiraProject = exports.saveJiraCredentials = exports.getJiraProjects = exports.getJiraCloudSites = exports.getJiraRefreshToken = exports.getJiraToken = exports.authorizeJira = void 0;
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * The formatted scopes of jira permissions being requested.
 */
var scopes = encodeURI([
    // Current Jira API version:
    "read:jira-work",
    "read:jira-user",
    "offline_access",
].join(" "));
/**
 * Runs a fetch call to the Atlassian API.
 *
 * @param args - The fetch parameters to use.
 * @return The returned data.
 */
function fetchAtlassian() {
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
                        throw Error("Unable to connect to Atlassian.");
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
 * Opens an external link to authorize Jira.
 */
function authorizeJira() {
    window.open("https://auth.atlassian.com/authorize?" +
        "audience=api.atlassian.com&" +
        ("client_id=" + process.env.VUE_APP_JIRA_CLIENT_ID + "&") +
        ("scope=" + scopes + "&") +
        ("redirect_uri=" + process.env.VUE_APP_JIRA_REDIRECT_LINK + "&") +
        ("state=" + store_1.sessionModule.getToken + "&") +
        "response_type=code&" +
        "prompt=consent");
}
exports.authorizeJira = authorizeJira;
/**
 * Exchanges an Atlassian access code for an API token.
 *
 * @param accessCode - The access code received from authorizing Jira.
 * @return The Jira access token.
 */
function getJiraToken(accessCode) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, fetchAtlassian("https://auth.atlassian.com/oauth/token", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        code: accessCode,
                        grant_type: "authorization_code",
                        client_id: process.env.VUE_APP_JIRA_CLIENT_ID,
                        client_secret: process.env.VUE_APP_JIRA_CLIENT_SECRET,
                        redirect_uri: process.env.VUE_APP_JIRA_REDIRECT_LINK
                    })
                })];
        });
    });
}
exports.getJiraToken = getJiraToken;
/**
 * Exchanges an Atlassian refresh token for an auth token.
 *
 * @param refreshToken - The atlassian refresh token.
 * @return The Jira access token.
 */
function getJiraRefreshToken(refreshToken) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, fetchAtlassian("https://auth.atlassian.com/oauth/token", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        refresh_token: refreshToken,
                        grant_type: "refresh_token",
                        client_id: process.env.VUE_APP_JIRA_CLIENT_ID,
                        client_secret: process.env.VUE_APP_JIRA_CLIENT_SECRET
                    })
                })];
        });
    });
}
exports.getJiraRefreshToken = getJiraRefreshToken;
/**
 * Exchanges an Atlassian access code for the list of cloud sites associated with the given user.
 *
 * @param accessToken - The access token received from authorizing Jira.
 * @return The Jira sites for this user.
 */
function getJiraCloudSites(accessToken) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, fetchAtlassian("https://api.atlassian.com/oauth/token/accessible-resources", {
                    method: "GET",
                    headers: {
                        Authorization: "Bearer " + accessToken
                    }
                })];
        });
    });
}
exports.getJiraCloudSites = getJiraCloudSites;
/**
 * TODO: update to internal GET `/projects/jira/{cloudId}`
 *
 * Returns all Jira projects for the given user and cloud site.
 *
 * @param accessToken - The access token received from authorizing Jira.
 * @param cloudId - The Jira cloud id to return projects for.
 * @return The user's projects associated with this cloud.
 */
function getJiraProjects(accessToken, cloudId) {
    return __awaiter(this, void 0, void 0, function () {
        var projects;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetchAtlassian("https://api.atlassian.com/ex/jira/" + cloudId + "/rest/api/3/project/search?expand=insight", {
                        method: "GET",
                        headers: {
                            Authorization: "Bearer " + accessToken,
                            Accept: "application/json"
                        }
                    })];
                case 1:
                    projects = _a.sent();
                    return [2 /*return*/, projects.values];
            }
        });
    });
}
exports.getJiraProjects = getJiraProjects;
/**
 * Saves a user's Jira credentials and primary organization.
 *
 * @param credentials - The access and refresh token received from authorizing Jira.
 */
function saveJiraCredentials(credentials) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.Endpoint.jiraCredentials, {
                    method: "POST",
                    body: JSON.stringify(credentials)
                })];
        });
    });
}
exports.saveJiraCredentials = saveJiraCredentials;
/**
 * Creates a new project based on a Jira project.
 *
 * @param cloudId - The Jira cloud id for this project.
 * @param projectId - The Jira project id to import.
 */
function createJiraProject(cloudId, projectId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.jiraProject, { cloudId: cloudId, projectId: projectId }), {
                    method: "POST"
                })];
        });
    });
}
exports.createJiraProject = createJiraProject;
