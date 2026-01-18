import { defineStore } from "pinia";
import { ref } from "vue";
import SockJS from "sockjs-client";
import Stomp, { Client, Frame, Message } from "webstomp-client";
import { StompApiHook, StompChannel } from "@/types";
import { formatTopic } from "@/util";
import { logStore } from "@/hooks";
import { WEBSOCKET_URL } from "@/api";
import { pinia } from "@/plugins";

const TIME_BETWEEN_RECONNECT = 2 * 1000; // every 2 seconds
const MAX_RECONNECT_ATTEMPTS = 20; // for a minute

/**
 * The hook with a client for connecting to the backend websocket server.
 */
export const useStompApi = defineStore("stompApi", (): StompApiHook => {
  const stompClient = ref<Client>();
  const isConnected = ref(false);
  const channels = ref<StompChannel[]>([]);
  const attempts = ref(0);

  /**
   * Returns the current stomp client, creating one if none exists.
   *
   * @throws If unable to connect to the server.
   * @return The stomp client.
   */
  function getStomp(): Client {
    if (!isConnected.value || stompClient.value === undefined) {
      logStore.onDevDebug("Creating new stomp client.");
      const sockJS = new SockJS(WEBSOCKET_URL());
      sockJS.onclose = () => {
        isConnected.value = false;
        stompClient.value = undefined;
        logStore.onDevError("Closing SockJS client.");
      };
      stompClient.value = Stomp.over(sockJS, { debug: false });
    }

    const client = stompClient.value;
    if (client === undefined) {
      throw Error("Stomp client is unavailable.");
    }

    return client;
  }

  /**
   * Setup up connection to back-end.
   */
  function connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const stomp = getStomp();

      if (stomp.connected) {
        isConnected.value = true;
        return resolve();
      }

      stomp.connect(
        { host: WEBSOCKET_URL() },
        () => {
          logStore.onDevDebug("Websocket connection successful.");
          isConnected.value = true;
          attempts.value = 0;
          return resolve();
        },
        (error: CloseEvent | Frame) => {
          logStore.onDevError(
            "Stomp has lost connection to server.\n" + JSON.stringify(error)
          );
          isConnected.value = false;
          attempts.value += 1;
          handleConnectionFailure();
          return reject();
        }
      );
    });
  }

  /**
   * Subscribes user to current stored topics. Useful on case of reconnection.
   */
  async function reconnect(): Promise<void> {
    await connect();
    const oldChannels = channels.value;
    channels.value = [];
    const subscriptionPromises = oldChannels.map((channel) =>
      subscribeTo(channel.topic, channel.handler)
    );
    await Promise.all(subscriptionPromises);
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
    try {
      await connect();

      if (topic.trim() === "") {
        throw Error("Expected destination to be non-empty.");
      }

      if (isSubscribedToTopic(topic)) {
        logStore.onDevDebug(formatTopic(topic) + " is already subscribed to.");
        return;
      }

      const stomp = getStomp();
      const subscription = stomp.subscribe(topic, handler);
      const channel: StompChannel = { subscription, topic, handler };

      channels.value.push(channel);
      logStore.onDevDebug("Subscribed to " + formatTopic(topic));
    } catch (error) {
      logStore.onDevError(
        `Failed to subscribe to topic ${formatTopic(topic)}: ${error}`
      );
      // Re-throw so callers can handle the error appropriately
      throw error;
    }
  }

  /**
   * Unsubscribes user from all subscriptions.
   */
  async function unsubscribe(targets: StompChannel[]): Promise<void> {
    if (!isConnected.value) {
      logStore.onDevDebug("Attempting to unsubscribe while disconnected.");
      return;
    }

    const channelTopics = targets.map((c) => c.topic);
    const persistentSubscriptions: StompChannel[] = [];
    channels.value.forEach((c) => {
      if (channelTopics.includes(c.topic)) {
        c.subscription.unsubscribe();
        logStore.onDevDebug("Unsubscribed from " + formatTopic(c.topic));
      } else {
        persistentSubscriptions.push(c);
      }
    });
    channels.value = persistentSubscriptions;
  }

  /**
   * Evaluates if topic is already subscribed to.
   * @param topic The topic to check.
   */
  function isSubscribedToTopic(topic: string): boolean {
    return channels.value
      .map((c) => c.topic === topic)
      .reduce((p, c) => p || c, false);
  }

  /**
   * Attempts to perpetually reconnect user until the maximum
   */
  function handleConnectionFailure() {
    if (attempts.value <= MAX_RECONNECT_ATTEMPTS) {
      setTimeout(async () => {
        await reconnect();
      }, TIME_BETWEEN_RECONNECT);
    } else {
      logStore.onDevDebug("Maximum number of reconnections reached.");
    }
  }

  return {
    isConnected,
    channels,
    connect,
    subscribeTo,
    unsubscribe,
    reconnect,
  };
});

export default useStompApi(pinia);
