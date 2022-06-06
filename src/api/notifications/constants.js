"use strict";
exports.__esModule = true;
exports.WEBSOCKET_URL = exports.RECONNECT_WAIT_TIME = exports.MAX_RECONNECT_ATTEMPTS = void 0;
var api_1 = require("@/api");
/**
 * The number of times to attempt to reconnect to server
 * if connection is lost.
 */
exports.MAX_RECONNECT_ATTEMPTS = 20;
/**
 * The amount of time to
 */
exports.RECONNECT_WAIT_TIME = 5000;
/**
 * Returns a WebSocket url resolving function. Use only after all modules
 * have been loaded.
 * @constructor
 */
var WEBSOCKET_URL = function () { return api_1.baseURL + "/websocket"; };
exports.WEBSOCKET_URL = WEBSOCKET_URL;
