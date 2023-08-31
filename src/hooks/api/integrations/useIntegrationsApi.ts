import { defineStore } from "pinia";

import { ref } from "vue";
import {
  InstallationSchema,
  IntegrationsApiHook,
  IOHandlerCallback,
} from "@/types";
import { useApi, integrationsStore, jobApiStore, projectStore } from "@/hooks";
import {
  getProjectInstallations,
  createGitHubProjectSync,
  createJiraProjectSync,
} from "@/api";
import { pinia } from "@/plugins";

export const useIntegrationsApi = defineStore(
  "integrationsApi",
  (): IntegrationsApiHook => {
    const integrationsApi = useApi("integrationsApi");

    const installations = ref<InstallationSchema[]>([]);

    async function handleReload(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await integrationsApi.handleRequest(async () => {
        installations.value = await getProjectInstallations(
          projectStore.projectId
        );
      }, callbacks);
    }

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
  }
);

export default useIntegrationsApi(pinia);
