import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import { PanelOpenState, PanelType } from "@/types";
import { artifactSelectionModule } from "@/store";

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
     * The open state for each type of panel.
     */
    isOpen: {
      [PanelType.left]: false,
      [PanelType.right]: false,
      [PanelType.artifactCreator]: false,
      [PanelType.errorDisplay]: false,
      [PanelType.artifactBody]: false,
      [PanelType.traceLinkCreator]: false,
    } as Record<PanelType, PanelOpenState>,
  }),
  getters: {},
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
    toggleRightPanel(): void {
      this.togglePanel(PanelType.right);
    },
    /**
     * Toggles whether the left panel is open.
     */
    toggleLeftPanel(): void {
      this.togglePanel(PanelType.left);
    },
    /**
     * Closes the side panels.
     */
    closeSidePanels(): void {
      this.closePanel(PanelType.left);
      this.closePanel(PanelType.right);
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
     * Opens the artifact creator to a specific node type.
     *
     * @param openTo - What to open to.
     */
    openArtifactCreatorTo(openTo: {
      type?: PanelOpenState;
      isNewArtifact?: boolean;
    }): void {
      const { type, isNewArtifact } = openTo;

      // TODO: remove module
      if (isNewArtifact) artifactSelectionModule.clearSelections();

      this.isOpen[PanelType.artifactCreator] = type || true;
    },
    /**
     * Closes the side panels.
     */
    closeArtifactCreator(): void {
      this.closePanel(PanelType.artifactCreator);
    },
  },
});

export default useApp(pinia);
