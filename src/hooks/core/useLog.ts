import { defineStore } from "pinia";

import { APIErrorBody, SnackbarMessage } from "@/types";
import { buildConfirmMessage, buildSnackbarMessage } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module controls logging and snackbar messages.
 */
export const useLog = defineStore("log", {
  state: () => ({
    /**
     * The current snackbar message.
     */
    message: buildSnackbarMessage(),
    /**
     * The current confirmation message.
     */
    confirmation: buildConfirmMessage(),
    /**
     * The timestamp of the last message displayed.
     */
    lastMessageTimestamp: 0,
    /**
     * A list of all messages displayed in the current session.
     */
    notifications: [] as SnackbarMessage[],
  }),
  getters: {},
  actions: {
    /**
     * Clears the current snackbar message.
     */
    clearMessage(): void {
      this.message = buildSnackbarMessage();
    },
    /**
     * Clears the current snackbar message.
     */
    clearConfirmation(): void {
      this.confirmation = buildConfirmMessage();
    },
    setMessage(message: SnackbarMessage): void {
      if (Date.now() - this.lastMessageTimestamp < 1000) {
        setTimeout(() => {
          this.message = message;
        }, 2000);
      } else {
        this.message = message;
      }

      this.lastMessageTimestamp = Date.now();
      this.notifications = [message, ...this.notifications];
    },
    /**
     * Creates a snackbar with the given message.
     *
     * @param message - The error message encountered.
     */
    onInfo(message: string): void {
      this.setMessage({ message, type: "info", errors: [] });
    },
    /**
     * Creates a snackbar for updating with the given message.
     *
     * @param message - The error message encountered.
     */
    onUpdate(message: string): void {
      this.setMessage({ message, type: "update", errors: [] });
    },
    /**
     * Creates a snackbar success with the given message.
     *
     * @param message - The error message encountered.
     */
    onSuccess(message: string): void {
      this.setMessage({ message, type: "success", errors: [] });
    },
    /**
     * Creates a snackbar warning with the given message.
     *
     * @param message - The error message encountered.
     */
    onWarning(message: string): void {
      this.setMessage({ message, type: "warning", errors: [] });
    },
    /**
     * Creates a snackbar error with the given message.
     *
     * @param message - The error message encountered.
     */
    onError(message: string): void {
      this.setMessage({ message, type: "error", errors: [] });
    },
    /**
     * Creates a snackbar error with the given server error.
     *
     * @param error - The error encountered.
     */
    onServerError(error: APIErrorBody | undefined): void {
      this.setMessage({
        message: error?.message || "An unexpected error occurred.",
        type: "error",
        errors: error?.errors || [],
      });
    },
    /**
     * Logs and prints message debug message to console when not in production.
     */
    onDevDebug(message: string): void {
      if (process.env.NODE_ENV !== "production") {
        console.log("DEBUG: " + message);
      }
    },
    /**
     * Logs and prints message to the console.
     */
    onDevInfo(message: string): void {
      if (process.env.NODE_ENV === "production") return;

      console.log(message);
    },
    /**
     * Logs and prints message to the console.
     */
    onDevError(message: string): void {
      if (process.env.NODE_ENV === "production") return;

      console.error(message);
    },
    /**
     * Opens a confirm window to run the given callback.
     *
     * @param title - The window's title.
     * @param body - The window's body.
     * @param statusCallback - The callback to run if confirmed or closed.
     */
    confirm(
      title: string,
      body: string,
      statusCallback: (confirmed: boolean) => Promise<void>
    ): void {
      this.$patch({
        confirmation: {
          type: "info",
          title,
          body,
          statusCallback,
        },
      });
    },
  },
});

export default useLog(pinia);
