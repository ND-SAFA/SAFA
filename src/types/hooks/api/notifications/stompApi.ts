import { Message, Subscription } from "webstomp-client";

/**
 * A hook for using stomp websocket messages.
 */
export interface StompApiHook {
  /**
   * Connects to BEND websocket server and tries to reconnect if
   * the connection fails.
   *
   * @param maxReconnectAttempts - The number of times to reconnect before failing.
   * @param reconnectWaitTime - The number of milliseconds to wait before reconnecting.
   * @param isReconnect - Whether this is a reconnect attempt.
   */
  connectStomp(
    maxReconnectAttempts?: number,
    reconnectWaitTime?: number,
    isReconnect?: boolean
  ): Promise<void>;
  /**
   * Subscribes to a websocket destination and returns the subscription.
   *
   * @param destination - The destination url to subscribe to.
   * @param callback - The callback to run when a message is received.
   */
  subscribeToStomp(
    destination: string,
    callback?: (message: Message) => void
  ): Promise<Subscription | undefined>;
  /**
   * Clears all subscriptions of the current user.
   */
  clearStompSubscriptions(): void;
}
