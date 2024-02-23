import { defineStore } from "pinia";

import { computed } from "vue";
import {
  CreateProjectApiHook,
  IOHandlerCallback,
  ProjectSchema,
} from "@/types";
import {
  integrationsStore,
  jobApiStore,
  orgStore,
  projectSaveStore,
  teamStore,
  useApi,
} from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  createGitHubProject,
  createJiraProject,
  createProjectCreationJob,
  createProjectUploadJob,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing create project API requests.
 */
export const useCreateProjectApi = defineStore(
  "createProjectApi",
  (): CreateProjectApiHook => {
    const createProjectApi = useApi("createProjectApi");

    const loading = computed(() => createProjectApi.loading);

    async function handleImport(callbacks: IOHandlerCallback): Promise<void> {
      const projectCreationRequest = projectSaveStore.creationRequest;
      const name = projectCreationRequest.project.name;

      await createProjectApi.handleRequest(
        async () => createProjectCreationJob(projectCreationRequest),
        {
          ...callbacks,
          onSuccess: async (job) => {
            await jobApiStore.handleCreate(job);
            await navigateTo(Routes.UPLOAD_STATUS);

            callbacks.onSuccess?.();
          },
          useAppLoad: true,
          success: `Project is being created: ${name}`,
          error: `Unable to import project: ${name}`,
        }
      );
    }

    async function handleBulkImport(
      project: Pick<
        ProjectSchema,
        "projectId" | "name" | "description" | "projectVersion"
      >,
      files: File[],
      summarize: boolean,
      callbacks: IOHandlerCallback
    ): Promise<void> {
      await createProjectApi.handleRequest(
        async () => {
          const job = await createProjectUploadJob({
            name: project.name,
            orgId: orgStore.orgId,
            teamId: teamStore.teamId,
            description: project.description,
            summarize,
            files,
          });

          await jobApiStore.handleCreate(job);
        },
        {
          ...callbacks,
          onComplete: async () => {
            await navigateTo(Routes.UPLOAD_STATUS);
            callbacks.onSuccess?.();
          },
          useAppLoad: true,
          success: `Project has been created: ${project.name}`,
          error: `Unable to create project: ${project.name}`,
        }
      );
    }

    async function handleJiraImport(
      callbacks: IOHandlerCallback
    ): Promise<void> {
      const installationId = integrationsStore.jiraOrganization?.id;
      const projectId = integrationsStore.jiraProject?.id;

      if (!installationId || !projectId) return;

      await createProjectApi.handleRequest(
        () =>
          createJiraProject(installationId, projectId, {
            orgId: orgStore.orgId,
            teamId: teamStore.teamId,
          }),
        {
          ...callbacks,
          onSuccess: async (job) => {
            integrationsStore.jiraProject = undefined;

            await jobApiStore.handleCreate(job);
            await navigateTo(Routes.UPLOAD_STATUS);

            callbacks.onSuccess?.();
          },
          useAppLoad: true,
          success: `Jira project has been created: ${projectId}`,
          error: `Unable to import jira project: ${projectId}`,
        }
      );
    }

    async function handleGitHubImport(
      callbacks: IOHandlerCallback
    ): Promise<void> {
      const repositoryName = integrationsStore.gitHubProject?.name;
      const owner = integrationsStore.gitHubProject?.owner;

      if (!repositoryName || !owner) return;

      await createProjectApi.handleRequest(
        () =>
          createGitHubProject(owner, repositoryName, {
            ...integrationsStore.gitHubConfig,
            orgId: orgStore.orgId,
            teamId: teamStore.teamId,
          }),
        {
          ...callbacks,
          onSuccess: async (job) => {
            integrationsStore.gitHubProject = undefined;

            await jobApiStore.handleCreate(job);
            await navigateTo(Routes.UPLOAD_STATUS);

            callbacks.onSuccess?.();
          },
          useAppLoad: true,
          success: `GitHub project has been created: ${repositoryName}`,
          error: `Unable to import GitHub project: ${repositoryName}`,
        }
      );
    }

    return {
      loading,
      handleImport,
      handleBulkImport,
      handleJiraImport,
      handleGitHubImport,
    };
  }
);

export default useCreateProjectApi(pinia);
