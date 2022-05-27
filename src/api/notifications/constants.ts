import { baseURL } from "@/api";

/**
 * The number of times to attempt to reconnect to server
 * if connection is lost.
 */
export const MAX_RECONNECT_ATTEMPTS = 20;
/**
 * The amount of time to
 */
export const RECONNECT_WAIT_TIME = 5000;
/**
 * Returns a WebSocket url resolving function. Use only after all modules
 * have been loaded.
 * @constructor
 */
export const WEBSOCKET_URL: () => string = () => `${baseURL}/websocket`;
