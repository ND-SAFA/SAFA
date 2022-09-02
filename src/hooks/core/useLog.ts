import { defineStore } from "pinia";

import { APIErrorBody, MessageType } from "@/types";
import { createConfirmDialogueMessage, createSnackbarMessage } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module controls logging and snackbar messages.
 */
export const useLog = defineStore("log", {
  state: () => ({
    /**
     * The current snackbar message.
     */
    message: createSnackbarMessage(),
    /**
     * The current confirmation message.
     */
    confirmation: createConfirmDialogueMessage(),
  }),
  getters: {},
  actions: {
    /**
     * Clears the current snackbar message.
     */
    clearMessage(): void {
      this.message = createSnackbarMessage();
    },
    /**
     * Clears the current snackbar message.
     */
    clearConfirmation(): void {
      this.confirmation = createConfirmDialogueMessage();
    },
    /**
     * Creates a snackbar with the given message.
     *
     * @param message - The error message encountered.
     */
    onInfo(message: string): void {
      this.message = { message, type: MessageType.INFO, errors: [] };
    },
    /**
     * Creates a snackbar for updating with the given message.
     *
     * @param message - The error message encountered.
     */
    onUpdate(message: string): void {
      this.message = { message, type: MessageType.UPDATE, errors: [] };
    },
    /**
     * Creates a snackbar success with the given message.
     *
     * @param message - The error message encountered.
     */
    onSuccess(message: string): void {
      this.message = { message, type: MessageType.SUCCESS, errors: [] };
    },
    /**
     * Creates a snackbar warning with the given message.
     *
     * @param message - The error message encountered.
     */
    onWarning(message: string): void {
      this.message = { message, type: MessageType.WARNING, errors: [] };
    },
    /**
     * Creates a snackbar error with the given message.
     *
     * @param message - The error message encountered.
     */
    onError(message: string): void {
      this.message = { message, type: MessageType.ERROR, errors: [] };
    },
    /**
     * Creates a snackbar error with the given server error.
     *
     * @param error - The error encountered.
     */
    onServerError(error: APIErrorBody | undefined): void {
      this.message = {
        message: error?.message || "An unexpected error occurred.",
        type: MessageType.ERROR,
        errors: error?.errors || [],
      };
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
  },
});

export default useLog(pinia);
