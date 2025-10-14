import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  GitHubApiHook,
  GitHubOrganizationSchema,
  GitHubProjectSchema,
  IOHandlerCallback,
} from "@/types";
import { useApi, integrationsStore } from "@/hooks";
import { getParam, QueryParams, removeParams } from "@/router";
import {
  getGitHubCredentials,
  getGitHubProjects,
  refreshGitHubCredentials,
  saveGitHubCredentials,
  authorizeGitHub,
  deleteGitHubCredentials,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing GitHub API requests.
 */
export const useGitHubApi = defineStore("gitHubApi", (): GitHubApiHook => {
  const githubApi = useApi("githubApi");

  const organizationList = ref<GitHubOrganizationSchema[]>([]);
  const projectList = ref<GitHubProjectSchema[]>([]);

  const loading = computed(() => githubApi.loading);

  function handleAuthRedirect(): void {
    authorizeGitHub(integrationsStore.validGitHubCredentials);
  }

  async function handleDeleteCredentials(): Promise<void> {
    await githubApi.handleRequest(async () => {
      await deleteGitHubCredentials();
      integrationsStore.validGitHubCredentials = false;
    });
  }

  async function handleVerifyCredentials(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    if (integrationsStore.validGitHubCredentials) return;

    const accessCode =
      getParam(QueryParams.TAB) === "github"
        ? getParam(QueryParams.INTEGRATION_TOKEN)
        : "";

    const onSuccess = () => {
      integrationsStore.validGitHubCredentials = true;
      removeParams();
      callbacks.onSuccess?.();
    };
    const onError = (e: Error) => {
      integrationsStore.validGitHubCredentials = false;
      callbacks.onError?.(e);
    };

    await githubApi.handleRequest(
      async () => {
        if (accessCode) {
          await saveGitHubCredentials(String(accessCode));
        } else {
          const valid = await getGitHubCredentials();

          if (valid) return;

          const refreshValid = await refreshGitHubCredentials();

          if (!refreshValid) {
            throw new Error("Invalid refresh");
          }
        }
      },
      {
        onSuccess,
        onError,
        error: accessCode ? "Unable to save GitHub access code." : undefined,
      }
    );
  }

  async function handleLoadProjects(
    callbacks: IOHandlerCallback<GitHubProjectSchema[]> = {}
  ): Promise<void> {
    await githubApi.handleRequest(async () => {
      integrationsStore.gitHubOrganization = undefined;
      organizationList.value = [];

      const projects = await getGitHubProjects();

      // Add organizations to the list based on the projects.
      projects.forEach(({ owner }) => {
        if (organizationList.value.find(({ id }) => id === owner)) return;

        organizationList.value.push({
          id: owner,
          name: owner,
        });
      });

      projectList.value = projects;

      return projects;
    }, callbacks);
  }

  return {
    organizationList,
    projectList,
    loading,
    handleAuthRedirect,
    handleDeleteCredentials,
    handleVerifyCredentials,
    handleLoadProjects,
  };
});

export default useGitHubApi(pinia);
