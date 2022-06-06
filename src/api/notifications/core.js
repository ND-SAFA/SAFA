"use strict";
exports.__esModule = true;
exports.clearSubscriptions = exports.connect = exports.stompClient = void 0;
var sockjs_client_1 = require("sockjs-client");
var webstomp_client_1 = require("webstomp-client");
var store_1 = require("@/store");
var constants_1 = require("@/api/notifications/constants");
/**
 * The WebSocket used to send messages.
 */
var sock;
/**
 * The interval used to synchronized possible conflicting re-connect attempts.
 * Note, subsequent reconnect calls can conflict with the reception of messages
 * so this is a guard rail.
 */
var reconnectInterval;
/**
 * The number of times a reconnect has been attempted since the connection
 * was lost.
 */
var nReconnectAttempts = 0;
/**
 * Returns the current stomp client, creating one if none exists.
 *
 * @param reconnect - Whether to create a new connection regardless
 * of websocket state.
 * @throws If unable to connect to the server.
 * @return The stomp client.
 */
function getStompClient(reconnect) {
    if (reconnect === void 0) { reconnect = false; }
    if (sock === undefined || exports.stompClient === undefined || reconnect) {
        try {
            sock = new sockjs_client_1["default"](constants_1.WEBSOCKET_URL(), { DEBUG: false });
            sock.onclose = function () {
                store_1.logModule.onDevMessage("Closing WebSocket.");
                connect().then();
            };
            exports.stompClient = webstomp_client_1["default"].over(sock, { debug: false });
        }
        catch (e) {
            if (!reconnect) {
                throw e;
            }
        }
    }
    return exports.stompClient;
}
/**
 * Connects to BEND websocket server and tries to reconnect if
 * the connection fails. Returns immediately.
 *
 * @param maxReconnectAttempts - The number of times to try to reconnect before
 * failing.
 * @param reconnectWaitTime - The number of milliseconds to wait before attempting
 * reconnect
 * @param isReconnect - Whether this is a reconnect attempt.
 */
function connect(maxReconnectAttempts, reconnectWaitTime, isReconnect) {
    if (maxReconnectAttempts === void 0) { maxReconnectAttempts = constants_1.MAX_RECONNECT_ATTEMPTS; }
    if (reconnectWaitTime === void 0) { reconnectWaitTime = constants_1.RECONNECT_WAIT_TIME; }
    if (isReconnect === void 0) { isReconnect = false; }
    return new Promise(function (resolve, reject) {
        var stomp = getStompClient(isReconnect);
        if (stomp.connected) {
            store_1.logModule.onDevMessage("Client is connected to WebSocket.");
            clearInterval(reconnectInterval);
            return resolve();
        }
        if (nReconnectAttempts > 0) {
            store_1.logModule.onDevMessage("Websocket reconnect attempt:" + nReconnectAttempts);
        }
        nReconnectAttempts++;
        stomp.connect({ host: constants_1.WEBSOCKET_URL() }, function () {
            if (nReconnectAttempts > 1) {
                store_1.logModule.onDevMessage("Web Socket reconnected to server.");
            }
            store_1.logModule.onDevMessage("Websocket connection successful.");
            store_1.logModule.onDevMessage("Subscriptions: " + JSON.stringify(stomp.subscriptions));
            clearInterval(reconnectInterval);
            nReconnectAttempts = 0;
            resolve();
        }, function () {
            store_1.logModule.onDevMessage("Re-connecting with WebSocket.");
            clearInterval(reconnectInterval);
            reconnectInterval = setInterval(function () {
                if (nReconnectAttempts < maxReconnectAttempts) {
                    connect(maxReconnectAttempts, reconnectWaitTime, true)
                        .then(resolve)["catch"](reject);
                }
                else {
                    clearInterval(reconnectInterval);
                    var error = "Web Socket lost connection to server, please reload page.";
                    store_1.logModule.onDevError(error);
                    reject(error);
                }
            }, reconnectWaitTime);
        });
    });
}
exports.connect = connect;
/**
 * Clears all subscriptions of the current user.
 */
function clearSubscriptions() {
    var stomp = getStompClient();
    var subscriptionIds = Object.keys(stomp.subscriptions);
    subscriptionIds.forEach(function (subId) { return stomp.unsubscribe(subId); });
}
exports.clearSubscriptions = clearSubscriptions;
