import { Ref } from "vue";
import { InstallationSchema, IOHandlerCallback } from "@/types";

/**
 * A hook for calling integrations API endpoints.
 */
export interface IntegrationsApiHook {
  /**
   * The installations affiliated with the current project.
   */
  installations: Ref<InstallationSchema[]>;
  /**
   * Handles loading installations affiliated with the current project.
   *
   * @param callbacks - Called once the action is complete.
   */
  handleLoadInstallations(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Syncs the current project with the selected installation's data.
   *
   * @param installation - The installation to sync data with.
   * @param isNew - Whether or not this is a new installation.
   * @param callbacks - Called once the action is complete.
   */
  handleSync(
    installation: Omit<InstallationSchema, "lastUpdate">,
    isNew?: boolean,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Creates a sync with a new installation.
   *
   * @param installationType - The installation type to sync data with.
   * @param callbacks - Called once the action is complete.
   */
  handleNewSync(
    installationType?: "Jira" | "GitHub",
    callbacks?: IOHandlerCallback
  ): Promise<void>;
}
