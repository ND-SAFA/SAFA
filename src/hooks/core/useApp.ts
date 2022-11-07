import { defineStore } from "pinia";

import {
  CreatorOpenState,
  GeneratorOpenState,
  PanelStateMap,
  PanelType,
} from "@/types";
import { pinia } from "@/plugins";
import selectionStore from "../graph/useSelection";
import logStore from "./useLog";

/**
 * This module defines state shared across the entire app.
 */
export const useApp = defineStore("app", {
  state: () => ({
    /**
     * Whether the app is currently loading, as a number of loading processes.
     */
    isLoading: 0,
    /**
     * Whether the app is currently saving.
     */
    isSaving: false,
    /**
     * Whether the app is currently saving.
     */
    runUpdate: undefined as (() => Promise<void>) | undefined,
    /**
     * The open state for each type of panel.
     */
    isOpen: {
      [PanelType.appPanel]: true,
      [PanelType.detailsPanel]: false,
      [PanelType.artifactCreator]: false,
      [PanelType.errorDisplay]: false,
      [PanelType.artifactBody]: false,
      [PanelType.traceLinkCreator]: false,
      [PanelType.traceLinkDraw]: false,
      [PanelType.traceLinkGenerator]: false,
    } as PanelStateMap,
  }),
  getters: {
    /**
     * @return Whether the left app panel is open.
     */
    isAppPanelOpen(): boolean {
      return this.isOpen[PanelType.appPanel];
    },
    /**
     * @return Whether the right details panel is open.
     */
    isDetailsPanelOpen(): boolean {
      return this.isOpen[PanelType.detailsPanel];
    },
    /**
     * @return Whether the artifact creator is open.
     */
    isArtifactCreatorOpen(): CreatorOpenState {
      return this.isOpen[PanelType.artifactCreator];
    },
    /**
     * @return Whether the error display is open.
     */
    isErrorDisplayOpen(): boolean {
      return this.isOpen[PanelType.errorDisplay];
    },
    /**
     * @return Whether the artifact body is open.
     */
    isArtifactBodyOpen(): boolean {
      return this.isOpen[PanelType.artifactBody];
    },
    /**
     * @return Whether the trace link creator is open.
     */
    isTraceLinkCreatorOpen(): boolean {
      return this.isOpen[PanelType.traceLinkCreator];
    },
    /**
     * @return Whether the trace link creator is open.
     */
    isTraceLinkGeneratorOpen(): GeneratorOpenState {
      return this.isOpen[PanelType.traceLinkGenerator];
    },
    /**
     * @return Whether trace link drawing is enabled.
     */
    isCreateLinkEnabled(): boolean {
      return this.isOpen[PanelType.traceLinkDraw];
    },
  },
  actions: {
    /**
     * Adds a loading process.
     */
    onLoadStart(): void {
      this.isLoading += 1;
    },
    /**
     * Removes a loading process.
     */
    onLoadEnd(): void {
      this.isLoading -= 1;
    },
    /**
     * Opens the given panel.
     *
     * @param panel - The type of panel.
     */
    openPanel(panel: PanelType): void {
      this.isOpen[panel] = true;
    },
    /**
     * Closes the given panel.
     *
     * @param panel - The type of panel.
     */
    closePanel(panel: PanelType): void {
      this.isOpen[panel] = false;
    },
    /**
     * Toggles the given panel.
     *
     * @param panel - The type of panel.
     */
    togglePanel(panel: PanelType): void {
      this.isOpen[panel] = !this.isOpen[panel];
    },
    /**
     * Toggles whether the right panel is open.
     */
    toggleAppPanel(): void {
      this.togglePanel(PanelType.appPanel);
    },
    /**
     * Toggles whether the details panel is open.
     */
    toggleDetailsPanel(): void {
      this.togglePanel(PanelType.detailsPanel);
    },
    /**
     * Closes the side panels.
     */
    closeSidePanels(): void {
      this.closePanel(PanelType.detailsPanel);
    },
    /**
     * Closes the side panels.
     */
    toggleErrorDisplay(): void {
      this.togglePanel(PanelType.errorDisplay);
    },
    /**
     * Toggles whether the artifact body modal is open.
     */
    toggleArtifactBody(): void {
      this.togglePanel(PanelType.artifactBody);
    },
    /**
     * Toggles whether the trace link creator is open.
     */
    toggleTraceLinkCreator(): void {
      this.togglePanel(PanelType.traceLinkCreator);
    },
    /**
     * Opens the trace link generator.
     */
    openTraceLinkGenerator(state: GeneratorOpenState): void {
      this.isOpen[PanelType.traceLinkGenerator] = state;
    },
    /**
     * Toggles whether the trace link generator is open.
     */
    closeTraceLinkGenerator(): void {
      this.closePanel(PanelType.traceLinkGenerator);
    },
    /**
     * Enables the draw link mode.
     */
    enableDrawLink(): void {
      this.openPanel(PanelType.traceLinkDraw);
    },
    /**
     * Disables the draw link mode.
     */
    disableDrawLink(): void {
      this.closePanel(PanelType.traceLinkDraw);
    },
    /**
     * Opens the artifact creator to a specific node type.
     *
     * @param openTo - What to open to.
     */
    openArtifactCreatorTo(openTo: {
      type?: CreatorOpenState;
      isNewArtifact?: boolean;
    }): void {
      const { type, isNewArtifact } = openTo;

      if (isNewArtifact) selectionStore.clearSelections();

      this.isOpen[PanelType.artifactCreator] = type || true;
    },
    /**
     * Closes the artifact creator.
     */
    closeArtifactCreator(): void {
      this.closePanel(PanelType.artifactCreator);
    },
    /**
     * Enqueues a new update to be loaded when the user is ready.
     *
     * @param update - A callback to run the update.
     */
    enqueueChanges(update: () => Promise<void>): void {
      this.runUpdate = update;

      logStore.onUpdate("Recent changes can be loaded.");
    },
    /**
     * Runs any pending changes to the app.
     */
    async loadAppChanges(): Promise<void> {
      try {
        this.onLoadStart();

        this.runUpdate?.();
      } finally {
        this.runUpdate = undefined;
        this.onLoadEnd();
      }
    },
  },
});

export default useApp(pinia);
