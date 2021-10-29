import type { Project } from "@/types/domain/project";
import { projectModule } from "@/store";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import { MessageType, PanelType } from "@/types/store";
import type { SnackbarMessage } from "@/types/store";

import type { PanelState } from "@/types/store";
import type { APIErrorBody } from "@/types/api";
export interface ChannelSubscriptionId {
  projectId?: string;
  versionId?: string;
}

@Module({ namespaced: true, name: "app" })
export default class ProjectModule extends VuexModule {
  snackbarMessage: SnackbarMessage | undefined = undefined;
  isLoading = false;
  isLeftOpen = false;
  isRightOpen = false;
  isErrorDisplayOpen = false;
  isArtifactCreatorOpen = false;

  @Action
  onLoadStart(): void {
    this.SET_IS_LOADING(true);
  }
  @Action
  onLoadEnd(): void {
    this.SET_IS_LOADING(false);
  }
  @Action
  onServerError(error: APIErrorBody): void {
    console.error(error.message);
    const { message, errors } = error;
    this.SET_MESSAGE({
      message,
      type: MessageType.ERROR,
      errors,
    });
  }
  @Action
  onError(message: string): void {
    console.error(message);
    this.SET_MESSAGE({ message, type: MessageType.ERROR, errors: [] });
  }
  @Action
  onMessage(message: string): void {
    console.log(message);
    this.SET_MESSAGE({ message, type: MessageType.INFO, errors: [] });
  }
  @Action
  onWarning(message: string): void {
    console.warn(message);
    this.SET_MESSAGE({ message, type: MessageType.WARNING, errors: [] });
  }
  @Action
  onSuccess(message: string): void {
    console.log(message);
    this.SET_MESSAGE({ message, type: MessageType.SUCCESS, errors: [] });
  }
  @Action
  toggleRightPanel(): void {
    this.TOGGLE_PANEL_STATE(PanelType.right);
  }
  @Action
  toggleLeftPanel(): void {
    this.TOGGLE_PANEL_STATE(PanelType.left);
  }
  @Action
  openPanel(panel: PanelType): void {
    if (panel === PanelType.artifactCreator) {
      const project: Project = projectModule.getProject;
      if (project.projectId === "") {
        this.onWarning(
          "Cannot create an artifact until a project is selected."
        );
        return;
      }
    }
    this.SET_PANEL_STATE({
      type: panel,
      isOpen: true,
    } as PanelState);
  }
  @Action
  closePanel(panel: PanelType): void {
    this.SET_PANEL_STATE({
      type: panel,
      isOpen: false,
    } as PanelState);
  }

  @Mutation
  SET_IS_LOADING(isLoading: boolean): void {
    this.isLoading = isLoading;
  }
  @Mutation
  SET_MESSAGE(message: SnackbarMessage): void {
    this.snackbarMessage = message;
  }
  @Mutation
  CLEAR_MESSAGE(): void {
    this.snackbarMessage = undefined;
  }
  @Mutation
  NOT_IMPLEMENTED_ERROR(): void {
    this.snackbarMessage = {
      message: "This feature is under construction",
      type: MessageType.WARNING,
      errors: [],
    };
  }
  @Mutation
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
  TOGGLE_PANEL_STATE(panel: PanelType): void {
    switch (panel) {
      case PanelType.left:
        this.isLeftOpen = !this.isLeftOpen;
        break;
      case PanelType.right:
        this.isRightOpen = !this.isRightOpen;
        break;
      default:
        throw Error(`${panel} has not been defined to be toggled`);
    }
  }

  get getMessage(): SnackbarMessage | undefined {
    return this.snackbarMessage;
  }
  get getIsLeftOpen(): boolean {
    return this.isLeftOpen;
  }
  get getIsRightOpen(): boolean {
    return this.isRightOpen;
  }
  get getIsArtifactCreatorOpen(): boolean {
    return this.isArtifactCreatorOpen;
  }
  get getIsErrorDisplayOpen(): boolean {
    return this.isErrorDisplayOpen;
  }
}
