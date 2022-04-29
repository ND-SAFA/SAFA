import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { PanelState } from "@/types";
import { FTANodeType, PanelType, SafetyCaseType } from "@/types";

@Module({ namespaced: true, name: "app" })
/**
 * This module defines state variables shared across the entire app.
 */
export default class ProjectModule extends VuexModule {
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
   * Whether currently in create trace link mode.
   */
  private isCreateLinkEnabled = false;
  /**
   * Whether the artifact creator is open.
   * If the value is set to a safety case or FTA node type, then the
   * artifact creator will open to that type set.
   */
  private isArtifactCreatorOpen: boolean | string = false;

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
   * Closes the side panels.
   */
  openErrorDisplay(): void {
    this.openPanel(PanelType.errorDisplay);
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
   * Closes the side panels.
   */
  closeSidePanels(): void {
    this.closePanel(PanelType.left);
    this.closePanel(PanelType.right);
  }

  @Action
  /**
   * Closes the side panels.
   */
  closeCreator(): void {
    this.closePanel(PanelType.artifactCreator);
  }

  @Action
  /**
   * Closes the side panels.
   */
  closeErrorDisplay(): void {
    this.closePanel(PanelType.errorDisplay);
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
    });
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
    });
  }

  @Action
  /**
   * Opens the artifact creator to a specific node type.
   *
   * @param type - The type of panel.
   */
  openArtifactCreatorTo(type?: SafetyCaseType | FTANodeType): void {
    this.SET_ARTIFACT_CREATOR(type || true);
  }

  @Mutation
  /**
   * Sets whether trace link draw mode is enabled.
   *
   * @param enabled - Whether to enable the draw mode.
   */
  SET_CREATE_LINK_ENABLED(enabled: boolean): void {
    this.isCreateLinkEnabled = enabled;
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
   * Sets the artifact creator state.
   *
   * @param isOpenOrType - The state of the artifact creator.
   */
  SET_ARTIFACT_CREATOR(isOpenOrType: boolean | string): void {
    this.isArtifactCreatorOpen = isOpenOrType;
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

  /**
   * @return Whether the app is currently loading.
   */
  get getIsLoading(): boolean {
    return this.isLoading;
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
  get getIsArtifactCreatorOpen(): boolean | string {
    return this.isArtifactCreatorOpen;
  }

  /**
   * @return Whether the error display is open.
   */
  get getIsErrorDisplayOpen(): boolean {
    return this.isErrorDisplayOpen;
  }

  /**
   * @return Whether trace link draw mode is currently enabled.
   */
  get getIsCreateLinkEnabled(): boolean {
    return this.isCreateLinkEnabled;
  }
}
