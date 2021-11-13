/**
 * Enumerates app store message types.
 */
export enum MessageType {
  INFO = "info",
  SUCCESS = "success",
  ERROR = "error",
  WARNING = "warning",
  CLEAR = "clear",
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
