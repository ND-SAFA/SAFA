/**
 * Enumerates app store message types.
 */
export enum MessageType {
  info = "info",
  update = "update",
  success = "success",
  error = "error",
  warning = "warning",
  clear = "clear",
}

/**
 * Defines a snackbar message.
 */
export interface SnackbarMessage {
  /**
   * A list of errors.
   */
  errors: string[];
  /**
   * The message text.
   */
  message: string;
  /**
   * The message type.
   */
  type: MessageType;
}
