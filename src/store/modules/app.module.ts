import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { PanelState } from "@/types";
import { PanelOpenState, PanelType } from "@/types";
import { artifactSelectionModule } from "@/store";

@Module({ namespaced: true, name: "app" })
/**
 * This module defines state variables shared across the entire app.
 */
export default class ProjectModule extends VuexModule {
  /**
   * Whether the app is currently loading, as a number of loading process.
   */
  private isLoading = 0;
  /**
   * Whether the app is currently saving.
   */
  private isSaving = false;
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
   * Whether the artifact creator is open, or the type of artifact to create.
   */
  private isArtifactCreatorOpen: PanelOpenState = false;
  /**
   * Whether the artifact body modal is open.
   */
  private isArtifactBodyOpen = false;
  /**
   * Whether the trace link creator is open.
   */
  private isTraceLinkCreatorOpen = false;

  @Action
  /**
   * Sets the app to loading.
   */
  onLoadStart(): void {
    this.SET_IS_LOADING(this.isLoading + 1);
  }

  @Action
  /**
   * Sets the app to no longer loading.
   */
  onLoadEnd(): void {
    this.SET_IS_LOADING(this.isLoading - 1);
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
  toggleErrorDisplay(): void {
    this.TOGGLE_PANEL_STATE(PanelType.errorDisplay);
  }

  @Action
  /**
   * Toggles whether the artifact body modal is open.
   */
  toggleArtifactBody(): void {
    this.TOGGLE_PANEL_STATE(PanelType.artifactBody);
  }

  @Action
  /**
   * Toggles whether the trace link creator is open.
   */
  toggleTraceLinkCreator(): void {
    this.TOGGLE_PANEL_STATE(PanelType.traceLinkCreator);
  }

  @Action
  /**
   * Opens the artifact creator to a specific node type.
   * @param openTo - What to open to.
   */
  openArtifactCreatorTo(openTo: {
    type?: PanelOpenState;
    isNewArtifact?: boolean;
  }): void {
    const { type, isNewArtifact } = openTo;

    if (isNewArtifact) artifactSelectionModule.clearSelections();

    this.SET_PANEL_STATE({
      type: PanelType.artifactCreator,
      isOpen: type || true,
    });
  }

  @Action
  /**
   * Closes the side panels.
   */
  closeArtifactCreator(): void {
    this.closePanel(PanelType.artifactCreator);
  }

  @Action
  /**
   * If a project is selected, opens the given panel.
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
   * @param panel - The type of panel.
   */
  closePanel(panel: PanelType): void {
    this.SET_PANEL_STATE({
      type: panel,
      isOpen: false,
    });
  }

  @Mutation
  /**
   * Sets whether trace link draw mode is enabled.
   */
  SET_CREATE_LINK_ENABLED(enabled: boolean): void {
    this.isCreateLinkEnabled = enabled;
  }

  @Mutation
  /**
   * Sets the current loading state.
   */
  SET_IS_LOADING(isLoading: number): void {
    this.isLoading = isLoading;
  }

  @Mutation
  /**
   * Sets the current saving state.
   */
  SET_IS_SAVING(isSaving: boolean): void {
    this.isSaving = isSaving;
  }

  @Mutation
  /**
   * Sets whether a panel is open or closed.
   * @param panelState - The panel type and whether it should be open.
   */
  SET_PANEL_STATE(panelState: PanelState): void {
    const { isOpen, type: panel } = panelState;
    const value = !!isOpen;

    if (panel === PanelType.left) {
      this.isLeftOpen = value;
    } else if (panel === PanelType.right) {
      this.isRightOpen = value;
    } else if (panel === PanelType.artifactCreator) {
      this.isArtifactCreatorOpen = isOpen;
    } else if (panel === PanelType.errorDisplay) {
      this.isErrorDisplayOpen = value;
    } else if (panel === PanelType.artifactBody) {
      this.isArtifactBodyOpen = value;
    } else if (panel === PanelType.traceLinkCreator) {
      this.isTraceLinkCreatorOpen = value;
    }
  }

  @Mutation
  /**
   * Toggles the open state of the given panel.
   */
  TOGGLE_PANEL_STATE(panel: PanelType): void {
    if (panel === PanelType.left) {
      this.isLeftOpen = !this.isLeftOpen;
    } else if (panel === PanelType.right) {
      this.isRightOpen = !this.isRightOpen;
    } else if (panel === PanelType.artifactBody) {
      this.isArtifactBodyOpen = !this.isArtifactBodyOpen;
    } else if (panel === PanelType.traceLinkCreator) {
      this.isTraceLinkCreatorOpen = !this.isTraceLinkCreatorOpen;
    }
  }

  /**
   * @return Whether the app is currently loading.
   */
  get getIsLoading(): boolean {
    return this.isLoading > 0;
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
   * @return Whether the artifact body is open.
   */
  get getIsArtifactBodyOpen(): boolean {
    return this.isArtifactBodyOpen;
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

  /**
   * @return Whether the artifact creator is open.
   */
  get getIsTraceLinkCreatorOpen(): boolean {
    return this.isTraceLinkCreatorOpen;
  }

  /**
   * @return Whether the app is currently saving.
   */
  get getIsSaving(): boolean {
    return this.isSaving;
  }
}
