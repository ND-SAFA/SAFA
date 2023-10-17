import { Message } from "webstomp-client";
import { Ref } from "vue";
import { StompChannel } from "@/types";

/**
 * A hook for using stomp websocket messages.
 */
export interface StompApiHook {
  isConnected: Ref<boolean>;
  channels: Ref<StompChannel[]>;

  /**
   * Connects to BEND websocket server and tries to reconnect if
   * the connection fails.
   *
   * @param isReconnect - Whether this is a reconnect attempt.
   */
  connect(isReconnect?: boolean): Promise<void>;

  /**
   * Subscribes to a websocket destination and returns the subscription.
   *
   * @param destination - The destination url to subscribe to.
   * @param callback - The callback to run when a message is received.
   */
  subscribeTo(
    destination: string,
    callback?: (message: Message) => void
  ): Promise<void>;

  /**
   * Unsubscribes from channels.
   */
  unsubscribe(channels: StompChannel[]): Promise<void>;

  /**
   * Attempts to resubscribe to last stored topics.
   */
  reconnect(): Promise<void>;
}
