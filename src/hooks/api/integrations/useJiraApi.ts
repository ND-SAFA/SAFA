import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  IOHandlerCallback,
  JiraApiHook,
  JiraOrganizationSchema,
  JiraProjectSchema,
} from "@/types";
import { useApi, integrationsStore } from "@/hooks";
import { getParam, QueryParams, removeParams } from "@/router";
import {
  getJiraCredentials,
  getJiraProjects,
  refreshJiraCredentials,
  saveJiraCredentials,
  getJiraInstallations,
  authorizeJira,
  deleteJiraCredentials,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing Jira API requests.
 */
export const useJiraApi = defineStore("jiraApi", (): JiraApiHook => {
  const jiraApi = useApi("jiraApi");

  const organizationList = ref<JiraOrganizationSchema[]>([]);
  const projectList = ref<JiraProjectSchema[]>([]);

  const loading = computed(() => jiraApi.loading);

  function handleAuthRedirect(): void {
    authorizeJira();
  }

  async function handleDeleteCredentials(): Promise<void> {
    await deleteJiraCredentials();
    integrationsStore.validJiraCredentials = false;
  }

  async function handleVerifyCredentials(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    if (integrationsStore.validJiraCredentials) return;

    const accessCode =
      getParam(QueryParams.TAB) === "jira"
        ? getParam(QueryParams.INTEGRATION_TOKEN)
        : "";

    const onSuccess = () => {
      integrationsStore.validJiraCredentials = true;
      removeParams();
      callbacks.onSuccess?.();
    };
    const onError = (e: Error) => {
      integrationsStore.validJiraCredentials = false;
      callbacks.onError?.(e);
    };

    await jiraApi.handleRequest(
      async () => {
        if (accessCode) {
          await saveJiraCredentials(String(accessCode));
        } else {
          const valid = await getJiraCredentials();

          if (valid) return;

          const refreshValid = await refreshJiraCredentials().catch(
            () => false
          );

          if (!refreshValid) {
            throw new Error("Invalid refresh");
          }
        }
      },
      {
        onSuccess,
        onError,
        error: accessCode ? "Unable to save Jira access code." : undefined,
      }
    );
  }

  async function handleLoadOrganizations(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await jiraApi.handleRequest(async () => {
      integrationsStore.jiraOrganization = undefined;
      organizationList.value = await getJiraInstallations();
    }, callbacks);
  }

  async function handleLoadProjects(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const installationId = integrationsStore.jiraOrganization?.id;

    if (!installationId) return;

    await jiraApi.handleRequest(async () => {
      integrationsStore.jiraProject = undefined;
      projectList.value = await getJiraProjects(installationId);
    }, callbacks);
  }

  return {
    organizationList,
    projectList,
    loading,
    handleAuthRedirect,
    handleDeleteCredentials,
    handleVerifyCredentials,
    handleLoadOrganizations,
    handleLoadProjects,
  };
});

export default useJiraApi(pinia);
