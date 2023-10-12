import { defineStore } from "pinia";
import { ref } from "vue";
import SockJS from "sockjs-client";
import Stomp, {
  Client,
  Message,
  Subscription,
  SubscriptionsMap,
} from "webstomp-client";
import { StompApiHook } from "@/types";
import { logStore, sessionStore } from "@/hooks";
import {
  fillEndpoint,
  MAX_RECONNECT_ATTEMPTS,
  RECONNECT_WAIT_TIME,
  WEBSOCKET_URL,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * The hook with a client for connecting to the backend websocket server.
 */
export const useStompApi = defineStore("stompApi", (): StompApiHook => {
  const stompClient = ref<Client>();
  const socket = ref<WebSocket>();
  const reconnectInterval = ref<NodeJS.Timeout>();
  const reconnectAttempts = ref(0);
  const isConnected = ref(false);
  const isAuthenticated = ref(false);

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
        socket.value = new SockJS(WEBSOCKET_URL());
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
        isConnected.value = true;
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
          isConnected.value = true;
          resolve();
        },
        () => {
          logStore.onDevInfo("Re-connecting with WebSocket.");
          isConnected.value = false;
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

  async function subscribeToStomp(
    destination: string,
    callback?: (message: Message) => void
  ): Promise<Subscription | undefined> {
    console.log("subscribing to stomp.");
    await connectStomp();

    const stomp = getStomp();

    if (!stomp) return;

    const userId = sessionStore.userId;
    const userTopic = fillEndpoint("userTopic", { userId });
    console.log("SUB:", destination);
    stomp.subscribe(userTopic, (m) => {
      isAuthenticated.value = true;
      console.log("USER MSG:", m);
    });
    return stomp.subscribe(destination, callback);
  }

  function clearStompSubscriptions(): void {
    console.log("clearing stomp");
    const stomp = getStomp();

    if (!stomp) return;

    const subscriptionIds = Object.keys(stomp.subscriptions);

    subscriptionIds.forEach((subId) => stomp.unsubscribe(subId));
  }

  function getSubscriptions(): SubscriptionsMap | undefined {
    const stomp = getStomp();
    return stomp?.subscriptions;
  }

  return {
    connectStomp,
    subscribeToStomp,
    clearStompSubscriptions,
    getSubscriptions,
    isConnected,
    isAuthenticated,
  };
});

export default useStompApi(pinia);
