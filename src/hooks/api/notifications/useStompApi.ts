import { defineStore } from "pinia";
import { ref } from "vue";
import SockJS from "sockjs-client";
import Stomp, { Client, Frame, Message, Subscription } from "webstomp-client";
import { StompApiHook } from "@/types";
import { logStore } from "@/hooks";
import { WEBSOCKET_URL } from "@/api";
import { pinia } from "@/plugins";

interface Channel {
  subscription: Subscription;
  topic: string;
  handler: (message: Message) => void;
}

/**
 * The hook with a client for connecting to the backend websocket server.
 */
export const useStompApi = defineStore("stompApi", (): StompApiHook => {
  const stompClient = ref<Client>();
  const socket = ref<WebSocket>();
  const isConnected = ref(false);
  const channels = ref<Channel[]>([]);

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

  /**
   * Setup up connection to back-end.
   * @param isReconnect Whether this is a reconnection attempt.
   */
  function connectStomp(isReconnect = false): Promise<void> {
    return new Promise((resolve, reject) => {
      const stomp = getStomp(isReconnect);

      if (!stomp) {
        const error = "Stomp returned null value:" + stomp;
        logStore.onDevError(error);
        return reject(error);
      }

      if (stomp.connected) {
        isConnected.value = true;
        return resolve();
      }

      stomp.connect(
        { host: WEBSOCKET_URL() },
        () => {
          logStore.onDevInfo("Websocket connection successful.");
          isConnected.value = true;
          if (isReconnect) {
            subscribeToTopics()
              .then(() => resolve())
              .catch(reject);
          }
          return resolve();
        },
        (error: CloseEvent | Frame) => {
          logStore.onDevError("Stomp has lost connection to server." + error);
          isConnected.value = false;
        }
      );
    });
  }

  /**
   * Subscribes user to current stored topics. Useful on case of reconnection.
   */
  function subscribeToTopics(): Promise<void[]> {
    const subscriptionPromises: Promise<void>[] = channels.value.map((c) => {
      return subscribeTo(c.topic, c.handler);
    });
    return Promise.all(subscriptionPromises);
  }

  /**
   * Subscribes to topic.
   * @param topic The topic to subscribe to.
   * @param handler Handles messages to topic.
   */
  async function subscribeTo(
    topic: string,
    handler: (message: Message) => void
  ): Promise<void> {
    await connectStomp();

    const stomp = getStomp();

    if (!stomp) {
      throw Error("Unable to get stomp client.");
    }

    if (topic.trim() === "") {
      throw Error("Expected destination to be non-empty.");
    }

    const subscription = stomp.subscribe(topic, handler);
    const channel: Channel = { subscription, topic, handler };
    channels.value.push(channel);
  }

  /**
   * Unsubscribes user from all subscriptions.
   */
  async function clearSubscriptions(): Promise<void> {
    if (!isConnected.value) {
      return;
    }
    const stomp = getStomp();

    if (!stomp) {
      logStore.onDevError("Stomp client is null on clearing subscriptions.");
      return;
    }
    channels.value.forEach((c) => c.subscription.unsubscribe());
    channels.value = [];
  }

  return {
    connectStomp,
    subscribeTo,
    clearSubscriptions,
    isConnected,
  };
});

export default useStompApi(pinia);
