import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { ConfirmDialogueMessage, PanelState } from "@/types/store/general";
import { APIErrorBody } from "@/types/api";
import { ConfirmationType, PanelType } from "@/types";
import type { SnackbarMessage } from "@/types/store/snackbar";
import { MessageType } from "@/types/store/snackbar";

const emptySnackbarMessage = {
  errors: [],
  message: "",
  type: MessageType.CLEAR,
};

const emptyConfirmationMessage = {
  type: ConfirmationType.CLEAR,
  title: "",
  body: "",
  statusCallback: () => null,
};

@Module({ namespaced: true, name: "app" })
/**
 * This module defines state variables shared across the entire app.
 */
export default class ProjectModule extends VuexModule {
  /**
   * The current snackbar message.
   */
  private snackbarMessage: SnackbarMessage = emptySnackbarMessage;
  /**
   * Whether the app is currently loading.
   */
  private isLoading = false;
  /**
   * Whether the left panel is open.
   */
  private isLeftOpen = false;
  /**
   * Whether the right panel is open.
   */
  private isRightOpen = false;
  /**
   * Whether the error display is open.
   */
  private isErrorDisplayOpen = false;
  /**
   * Whether the artifact creator is open.
   */
  private isArtifactCreatorOpen = false;

  /**
   * Whether the confirmation modal is open.
   */
  private confirmationMessage: ConfirmDialogueMessage =
    emptyConfirmationMessage;

  @Action
  /**
   * Sets the app to loading.
   */
  onLoadStart(): void {
    this.SET_IS_LOADING(true);
  }

  @Action
  /**
   * Sets the app to no longer loading.
   */
  onLoadEnd(): void {
    this.SET_IS_LOADING(false);
  }

  @Action
  /**
   * Creates a snackbar error message with the given server error.
   *
   * @param error - The error encountered.
   */
  onServerError(error: APIErrorBody): void {
    const { message, errors } = error;

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
    console.error(message);
    this.SET_MESSAGE({ message, type: MessageType.ERROR, errors: [] });
  }

  @Action
  /**
   * Creates a snackbar information message with the given message.
   *
   * @param message - The message to display.
   */
  onInfo(message: string): void {
    console.log(message);
    this.SET_MESSAGE({ message, type: MessageType.INFO, errors: [] });
  }

  @Action
  /**
   * Creates a snackbar warning message with the given message.
   *
   * @param message - The message to display.
   */
  onWarning(message: string): void {
    console.warn(message);
    this.SET_MESSAGE({ message, type: MessageType.WARNING, errors: [] });
  }

  @Action
  /**
   * Creates a snackbar success message with the given message.
   *
   * @param message - The message to display.
   */
  onSuccess(message: string): void {
    console.log(message);
    this.SET_MESSAGE({ message, type: MessageType.SUCCESS, errors: [] });
  }

  @Action
  /**
   * Toggles whether the right panel is open.
   */
  toggleRightPanel(): void {
    this.TOGGLE_PANEL_STATE(PanelType.right);
  }

  @Action
  /**
   * Toggles whether the left panel is open.
   */
  toggleLeftPanel(): void {
    this.TOGGLE_PANEL_STATE(PanelType.left);
  }

  @Action
  /**
   * If a project is selected, opens the given panel.
   *
   * @param panel - The type of panel.
   */
  openPanel(panel: PanelType): void {
    this.SET_PANEL_STATE({
      type: panel,
      isOpen: true,
    } as PanelState);
  }

  @Action
  /**
   * Closes the given panel.
   *
   * @param panel - The type of panel.
   */
  closePanel(panel: PanelType): void {
    this.SET_PANEL_STATE({
      type: panel,
      isOpen: false,
    } as PanelState);
  }

  @Mutation
  /**
   * Sets the current loading state.
   *
   * @param isLoading - Whether the app is loading.
   */
  SET_IS_LOADING(isLoading: boolean): void {
    this.isLoading = isLoading;
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
   * Sets whether a panel is open or closed.
   *
   * @param panelState - The panel type and whether it should be open.
   */
  SET_PANEL_STATE(panelState: PanelState): void {
    const { isOpen } = panelState;

    switch (panelState.type) {
      case PanelType.left:
        this.isLeftOpen = isOpen;
        break;
      case PanelType.right:
        this.isRightOpen = isOpen;
        break;
      case PanelType.artifactCreator:
        this.isArtifactCreatorOpen = isOpen;
        break;
      case PanelType.errorDisplay:
        this.isErrorDisplayOpen = isOpen;
        break;
      default:
        throw Error("Unrecognized panel: " + panelState.type);
    }
  }

  @Mutation
  /**
   * Toggles the open state of the given panel.
   *
   * @param panel - The panel type to toggle.
   */
  TOGGLE_PANEL_STATE(panel: PanelType): void {
    switch (panel) {
      case PanelType.left:
        this.isLeftOpen = !this.isLeftOpen;
        break;
      case PanelType.right:
        this.isRightOpen = !this.isRightOpen;
        break;
      default:
        throw Error(`${panel} cannot be toggled`);
    }
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
    this.confirmationMessage = emptyConfirmationMessage;
  }

  /**
   * @return Whether the app is currently loading.
   */
  get getIsLoading(): boolean {
    return this.isLoading;
  }

  /**
   * @return The current snackbar message.
   */
  get getMessage(): SnackbarMessage | undefined {
    return this.snackbarMessage;
  }

  /**
   * @return Whether the left panel is open.
   */
  get getIsLeftOpen(): boolean {
    return this.isLeftOpen;
  }

  /**
   * @return Whether the right panel is open.
   */
  get getIsRightOpen(): boolean {
    return this.isRightOpen;
  }

  /**
   * @return Whether the artifact creator is open.
   */
  get getIsArtifactCreatorOpen(): boolean {
    return this.isArtifactCreatorOpen;
  }

  /**
   * @return Whether the error display is open.
   */
  get getIsErrorDisplayOpen(): boolean {
    return this.isErrorDisplayOpen;
  }

  /**
   * @return Whether the artifact creator is open.
   */
  get getConfirmationMessage(): ConfirmDialogueMessage | undefined {
    return this.confirmationMessage;
  }
}
