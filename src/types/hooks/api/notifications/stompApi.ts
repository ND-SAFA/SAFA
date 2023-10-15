import { Message } from "webstomp-client";
import { Ref } from "vue";

/**
 * A hook for using stomp websocket messages.
 */
export interface StompApiHook {
  isConnected: Ref<boolean>;

  /**
   * Connects to BEND websocket server and tries to reconnect if
   * the connection fails.
   *
   * @param isReconnect - Whether this is a reconnect attempt.
   */
  connectStomp(isReconnect?: boolean): Promise<void>;

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
   * Clears all subscriptions of the current user.
   */
  clearSubscriptions(): Promise<void>;
}
