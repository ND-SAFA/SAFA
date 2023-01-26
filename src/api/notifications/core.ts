import SockJS from "sockjs-client";
import Stomp, { Client } from "webstomp-client";
import { logStore } from "@/hooks";
import {
  MAX_RECONNECT_ATTEMPTS,
  RECONNECT_WAIT_TIME,
  WEBSOCKET_URL,
} from "@/api/notifications/constants";

/**
 * The singleton client for connecting to the backend websocket server.
 */
export let stompClient: Client;

/**
 * The WebSocket used to send messages.
 */
let sock: WebSocket;
/**
 * The interval used to synchronized possible conflicting re-connect attempts.
 * Note, subsequent reconnect calls can conflict with the reception of messages
 * so this is a guard rail.
 */
let reconnectInterval: NodeJS.Timeout;
/**
 * The number of times a reconnect has been attempted since the connection
 * was lost.
 */
let nReconnectAttempts = 0;

/**
 * Returns the current stomp client, creating one if none exists.
 *
 * @param reconnect - Whether to create a new connection regardless
 * of websocket state.
 * @throws If unable to connect to the server.
 * @return The stomp client.
 */
function getStompClient(reconnect = false): Client {
  if (sock === undefined || stompClient === undefined || reconnect) {
    try {
      sock = new SockJS(WEBSOCKET_URL(), { DEBUG: false });
      sock.onclose = () => {
        logStore.onDevInfo("Closing WebSocket.");
        connect().then();
      };
      stompClient = Stomp.over(sock, { debug: false });
    } catch (e) {
      if (!reconnect) {
        throw e;
      }
    }
  }

  return stompClient;
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
export function connect(
  maxReconnectAttempts: number = MAX_RECONNECT_ATTEMPTS,
  reconnectWaitTime: number = RECONNECT_WAIT_TIME,
  isReconnect = false
): Promise<void> {
  return new Promise((resolve, reject) => {
    const stomp = getStompClient(isReconnect);

    if (stomp.connected) {
      logStore.onDevInfo("Client is connected to WebSocket.");
      clearInterval(reconnectInterval);
      return resolve();
    }

    if (nReconnectAttempts > 0) {
      logStore.onDevInfo(`Websocket reconnect attempt:${nReconnectAttempts}`);
    }

    nReconnectAttempts++;

    stomp.connect(
      { host: WEBSOCKET_URL() },
      () => {
        if (nReconnectAttempts > 1) {
          logStore.onDevInfo("Web Socket reconnected to server.");
        }
        logStore.onDevInfo("Websocket connection successful.");
        logStore.onDevInfo(
          `Subscriptions: ${JSON.stringify(stomp.subscriptions)}`
        );
        clearInterval(reconnectInterval);
        nReconnectAttempts = 0;
        resolve();
      },
      () => {
        logStore.onDevInfo("Re-connecting with WebSocket.");
        clearInterval(reconnectInterval);
        reconnectInterval = setInterval(function () {
          if (nReconnectAttempts < maxReconnectAttempts) {
            connect(maxReconnectAttempts, reconnectWaitTime, true)
              .then(resolve)
              .catch(reject);
          } else {
            clearInterval(reconnectInterval);
            const error =
              "Web Socket lost connection to server, please reload page.";
            logStore.onDevError(error);
            reject(error);
          }
        }, reconnectWaitTime);
      }
    );
  });
}

/**
 * Clears all subscriptions of the current user.
 */
export function clearSubscriptions(): void {
  const stomp = getStompClient();
  const subscriptionIds = Object.keys(stomp.subscriptions);

  subscriptionIds.forEach((subId) => stomp.unsubscribe(subId));
}
