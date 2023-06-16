import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  IOHandlerCallback,
  JiraOrganizationSchema,
  JiraProjectSchema,
} from "@/types";
import { useApi, integrationsStore } from "@/hooks";
import { getParam, QueryParams } from "@/router";
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

export const useIntegrationsApi = defineStore("integrationsApi", () => {
  const jiraApi = useApi("jiraApi");

  const organizationList = ref<JiraOrganizationSchema[]>([]);
  const projectList = ref<JiraProjectSchema[]>([]);

  const loading = computed(() => jiraApi.loading);

  /**
   * Opens the Jira authentication window.
   */
  function handleAuthRedirect(): void {
    authorizeJira();
  }

  /**
   * Clears the saved Jira credentials.
   */
  async function handleDeleteCredentials(): Promise<void> {
    await deleteJiraCredentials();
    integrationsStore.validJiraCredentials = false;
  }

  /**
   * Handles Jira authentication when the app loads.
   *
   * @param callbacks - Called once the action is complete.
   */
  async function handleVerifyCredentials(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const accessCode =
      getParam(QueryParams.TAB) === "jira"
        ? getParam(QueryParams.JIRA_TOKEN)
        : "";

    const onSuccess = () => {
      integrationsStore.validJiraCredentials = true;
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
      { onSuccess, onError },
      {
        error: accessCode
          ? "Unable to save Jira access code."
          : "Unable to refresh Jira credentials.",
      }
    );
  }

  /**
   * Loads Jira installations.
   *
   * @param callbacks - Called once the action is complete.
   */
  async function handleLoadOrganizations(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await jiraApi.handleRequest(async () => {
      integrationsStore.jiraOrganization = undefined;
      organizationList.value = await getJiraInstallations();
    }, callbacks);
  }

  /**
   * Loads Jira projects and sets the currently selected cloud id.
   *
   * @param callbacks - Called once the action is complete.
   */
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

export default useIntegrationsApi(pinia);
