import { defineStore } from "pinia";

import { DetailsOpenState, PopupStateMap, PopupType } from "@/types";
import { pinia } from "@/plugins";
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
     * The open state for each popup.
     */
    popups: {
      errorModal: false,
      navPanel: false,
      detailsPanel: false,
      saveOrg: false,
      saveTeam: false,
      saveProject: false,
      editProject: false,
      moveProject: false,
      deleteProject: false,
      saveArtifact: false,
      saveTrace: false,
      drawTrace: false,
    } as PopupStateMap,
  }),
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
     * Opens the given popup.
     *
     * @param popup - The type of popup.
     */
    open(popup: PopupType): void {
      this.popups[popup] = true;
    },
    /**
     * Closes the given popup.
     *
     * @param popup - The type of popup.
     */
    close(popup: PopupType): void {
      this.popups[popup] = false;
    },
    /**
     * Toggles the given popup.
     *
     * @param popup - The type of popup.
     */
    toggle(popup: PopupType): void {
      this.popups[popup] = !this.popups[popup];
    },

    /**
     * Closes the side panels.
     */
    closeSidePanels(): void {
      this.close("detailsPanel");
      this.close("saveArtifact");
    },
    /**
     * Opens the details panel.
     * @param state - The type of content to open.
     */
    openDetailsPanel(state: DetailsOpenState): void {
      this.popups.detailsPanel = state;
      this.popups.navPanel = false;
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
