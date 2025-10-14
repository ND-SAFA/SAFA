/**
 * Enumerates app store message types.
 */
export type MessageType =
  | "info"
  | "update"
  | "success"
  | "error"
  | "warning"
  | "clear";

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
