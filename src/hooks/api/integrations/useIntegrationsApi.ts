import { defineStore } from "pinia";

import { ref } from "vue";
import { InstallationSchema, IOHandlerCallback } from "@/types";
import { useApi, integrationsStore, jobApiStore, projectStore } from "@/hooks";
import {
  getProjectInstallations,
  createGitHubProjectSync,
  createJiraProjectSync,
} from "@/api";
import { pinia } from "@/plugins";

export const useIntegrationsApi = defineStore("integrationsApi", () => {
  const integrationsApi = useApi("integrationsApi");

  const installations = ref<InstallationSchema[]>([]);

  /**
   * Handles loading installations affiliated with the current project.
   *
   * @param callbacks - Called once the action is complete.
   */
  async function handleReload(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await integrationsApi.handleRequest(async () => {
      installations.value = await getProjectInstallations(
        projectStore.projectId
      );
    }, callbacks);
  }

  /**
   * Syncs the current project with the selected installation's data.
   *
   * @param installation - The installation to sync data with.
   * @param callbacks - Called once the action is complete.
   */
  async function handleSync(
    installation: Omit<InstallationSchema, "lastUpdate">,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await integrationsApi.handleRequest(
      async () => {
        const job =
          installation.type === "GITHUB"
            ? await createGitHubProjectSync(
                projectStore.versionId,
                installation.installationOrgId,
                installation.installationId,
                integrationsStore.gitHubConfig
              )
            : await createJiraProjectSync(
                projectStore.versionId,
                installation.installationOrgId,
                installation.installationId
              );

        await jobApiStore.handleCreate(job);
      },
      {
        ...callbacks,
        success: `Integration data is being synced: ${installation.installationId}. 
       You'll receive a notification once data has completed syncing.`,
        error: `Unable to sync integration data.`,
      }
    );
  }

  /**
   * Creates a sync with a new installation.
   *
   * @param installationType - The installation type to sync data with.
   * @param callbacks - Called once the action is complete.
   */
  async function handleNewSync(
    installationType?: "Jira" | "GitHub",
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await handleSync(
      installationType === "Jira"
        ? {
            type: "JIRA",
            installationOrgId: integrationsStore.jiraOrganization?.id || "",
            installationId: integrationsStore.jiraProject?.id || "",
          }
        : {
            type: "GITHUB",
            installationOrgId: integrationsStore.gitHubOrganization?.id || "",
            installationId: integrationsStore.gitHubProject?.name || "",
          },
      callbacks
    );
  }

  return {
    installations,
    handleReload,
    handleSync,
    handleNewSync,
  };
});

export default useIntegrationsApi(pinia);
