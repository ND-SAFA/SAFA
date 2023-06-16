import { defineStore } from "pinia";
import { ref } from "vue";
import SockJS from "sockjs-client";
import Stomp, { Client, Message, Subscription } from "webstomp-client";

import { logStore } from "@/hooks";
import {
  MAX_RECONNECT_ATTEMPTS,
  RECONNECT_WAIT_TIME,
  WEBSOCKET_URL,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * The singleton client for connecting to the backend websocket server.
 */
export const useStompApi = defineStore("stompApi", () => {
  const stompClient = ref<Client>();
  const socket = ref<WebSocket>();
  const reconnectInterval = ref<NodeJS.Timeout>();
  const reconnectAttempts = ref(0);

  /**
   * Returns the current stomp client, creating one if none exists.
   *
   * @param reconnect - Whether to create a new connection regardless
   * of websocket state.
   * @throws If unable to connect to the server.
   * @return The stomp client.
   */
  function getStomp(reconnect = false): Client | undefined {
    if (
      socket.value === undefined ||
      stompClient.value === undefined ||
      reconnect
    ) {
      try {
        socket.value = new SockJS(WEBSOCKET_URL(), { DEBUG: false });
        socket.value.onclose = () => {
          logStore.onDevInfo("Closing WebSocket.");
          connectStomp().then();
        };
        stompClient.value = Stomp.over(socket.value, { debug: false });
      } catch (e) {
        if (!reconnect) {
          throw e;
        }
      }
    }

    return stompClient.value;
  }

  /**
   * Connects to BEND websocket server and tries to reconnect if
   * the connection fails.
   *
   * @param maxReconnectAttempts - The number of times to reconnect before failing.
   * @param reconnectWaitTime - The number of milliseconds to wait before reconnecting.
   * @param isReconnect - Whether this is a reconnect attempt.
   */
  function connectStomp(
    maxReconnectAttempts: number = MAX_RECONNECT_ATTEMPTS,
    reconnectWaitTime: number = RECONNECT_WAIT_TIME,
    isReconnect = false
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      const stomp = getStomp(isReconnect);

      if (!stomp) return;

      if (stomp.connected) {
        logStore.onDevInfo("Client is connected to WebSocket.");
        clearInterval(reconnectInterval.value);
        return resolve();
      }

      if (reconnectAttempts.value > 0) {
        logStore.onDevInfo(
          `Websocket reconnect attempt:${reconnectAttempts.value}`
        );
      }

      reconnectAttempts.value++;

      stomp.connect(
        { host: WEBSOCKET_URL() },
        () => {
          logStore.onDevInfo(
            "Websocket connection successful. " +
              `Subscriptions: ${JSON.stringify(stomp.subscriptions)}`
          );

          clearInterval(reconnectInterval.value);

          reconnectAttempts.value = 0;
          resolve();
        },
        () => {
          logStore.onDevInfo("Re-connecting with WebSocket.");

          clearInterval(reconnectInterval.value);

          reconnectInterval.value = setInterval(function () {
            if (reconnectAttempts.value < maxReconnectAttempts) {
              connectStomp(maxReconnectAttempts, reconnectWaitTime, true)
                .then(resolve)
                .catch(reject);
            } else {
              clearInterval(reconnectInterval.value);

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
   * Subscribes to a websocket destination and returns the subscription.
   *
   * @param destination - The destination url to subscribe to.
   * @param callback - The callback to run when a message is received.
   */
  async function subscribeToStomp(
    destination: string,
    callback?: (message: Message) => void
  ): Promise<Subscription | undefined> {
    await connectStomp();

    const stomp = getStomp();

    if (!stomp) return;

    return stomp.subscribe(destination, callback);
  }

  /**
   * Clears all subscriptions of the current user.
   */
  function clearStompSubscriptions(): void {
    const stomp = getStomp();

    if (!stomp) return;

    const subscriptionIds = Object.keys(stomp.subscriptions);

    subscriptionIds.forEach((subId) => stomp.unsubscribe(subId));
  }

  return {
    getStomp,
    connectStomp,
    subscribeToStomp,
    clearStompSubscriptions,
  };
});

export default useStompApi(pinia);
