import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import { MessageType } from "@/types";
import type {
  SnackbarMessage,
  APIErrorBody,
  ConfirmDialogueMessage,
} from "@/types";
import { createConfirmDialogueMessage, createSnackbarMessage } from "@/util";

@Module({ namespaced: true, name: "snackbar" })
/**
 * This module controls snackbar messages.
 */
export default class SnackbarModule extends VuexModule {
  /**
   * The current snackbar message.
   */
  private snackbarMessage = createSnackbarMessage();
  /**
   * Whether the confirmation modal is open.
   */
  private confirmationMessage = createConfirmDialogueMessage();
  /**
   * A list of dev messages.
   */
  private devMessages: string[] = [];

  @Action
  /**
   * Creates a snackbar error message with the given server error.
   *
   * @param error - The error encountered.
   */
  onServerError(error: APIErrorBody | undefined): void {
    const { message, errors } = error || {
      message: "An unexpected error occurred.",
      errors: [],
    };

    this.SET_MESSAGE({
      message,
      type: MessageType.ERROR,
      errors,
    });
  }

  @Action
  /**
   * Creates a snackbar error message with the given message.
   *
   * @param message - The error message encountered.
   */
  onError(message: string): void {
    this.SET_MESSAGE({ message, type: MessageType.ERROR, errors: [] });
  }

  @Action
  /**
   * Creates a snackbar information message with the given message.
   *
   * @param message - The message to display.
   */
  onInfo(message: string): void {
    this.SET_MESSAGE({ message, type: MessageType.INFO, errors: [] });
  }

  @Action
  /**
   * Creates a snackbar warning message with the given message.
   *
   * @param message - The message to display.
   */
  onWarning(message: string): void {
    this.SET_MESSAGE({ message, type: MessageType.WARNING, errors: [] });
  }

  @Action
  /**
   * Creates a snackbar success message with the given message.
   *
   * @param message - The message to display.
   */
  onSuccess(message: string): void {
    this.SET_MESSAGE({ message, type: MessageType.SUCCESS, errors: [] });
  }

  @Action
  /**
   * Logs and prints message to the console.
   */
  onDevMessage(message: string): void {
    // console.log(message);
    this.ADD_DEV_MESSAGE(`Info: ${message}`);
  }

  @Action
  /**
   * Logs and prints warning to the console.
   */
  onDevWarning(message: string): void {
    console.warn(message);
    this.ADD_DEV_MESSAGE(`Warning: ${message}`);
  }

  @Action
  /**
   * Logs and prints error to the console.
   */
  onDevError(message: string): void {
    console.error(message);
    this.ADD_DEV_MESSAGE(`Error: ${message}`);
  }

  @Mutation
  /**
   * Sets the current snackbar message.
   *
   * @param message - The message to display.
   */
  ADD_DEV_MESSAGE(message: string): void {
    this.devMessages = [...this.devMessages, message];
  }

  @Mutation
  /**
   * Sets the current snackbar message.
   *
   * @param message - The message to display.
   */
  SET_MESSAGE(message: SnackbarMessage): void {
    this.snackbarMessage = message;
  }

  @Mutation
  /**
   * Clears the current snackbar message.
   */
  CLEAR_MESSAGE(): void {
    this.snackbarMessage = {
      ...this.snackbarMessage,
      type: MessageType.CLEAR,
    };
  }

  @Mutation
  /**
   * Sets a snackbar message that the current feature isn't implemented.
   */
  NOT_IMPLEMENTED_ERROR(): void {
    this.snackbarMessage = {
      message: "This feature is under construction",
      type: MessageType.WARNING,
      errors: [],
    };
  }

  @Mutation
  /**
   * Shows message in confirmation box to user, returns whether confirmed or not.
   *
   */
  SET_CONFIRMATION_MESSAGE(message: ConfirmDialogueMessage): void {
    this.confirmationMessage = message;
  }

  @Mutation
  /**
   * Shows message in confirmation box to user, returns whether confirmed or not.
   *
   */
  CLEAR_CONFIRMATION_MESSAGE(): void {
    this.confirmationMessage = createConfirmDialogueMessage();
  }

  /**
   * @return The current snackbar message.
   */
  get getMessage(): SnackbarMessage | undefined {
    return this.snackbarMessage;
  }

  /**
   * @return THe current confirmation message.
   */
  get getConfirmationMessage(): ConfirmDialogueMessage | undefined {
    return this.confirmationMessage;
  }
}
