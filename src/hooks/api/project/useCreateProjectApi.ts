import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, ProjectSchema } from "@/types";
import {
  integrationsStore,
  jobApiStore,
  projectSaveStore,
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

export const useCreateProjectApi = defineStore("createProjectApi", () => {
  const createProjectApi = useApi("createProjectApi");

  const loading = computed(() => createProjectApi.loading);

  /**
   * Creates a new project, sets related app state, and logs the status.
   *
   * @param onSuccess - Called if the action is successful.
   * @param onError - Called if the action fails.
   */
  async function handleImport({
    onSuccess,
    onError,
  }: IOHandlerCallback): Promise<void> {
    const projectCreationRequest = projectSaveStore.creationRequest;
    const name = projectCreationRequest.project.name;

    await createProjectApi.handleRequest(
      async () => createProjectCreationJob(projectCreationRequest),
      {
        onSuccess: async (job) => {
          await jobApiStore.handleCreate(job);
          await navigateTo(Routes.UPLOAD_STATUS);

          onSuccess?.();
        },
        onError,
      },
      {
        useAppLoad: true,
        success: `Project is being created: ${name}`,
        error: `Unable to import project: ${name}`,
      }
    );
  }

  /**
   * Creates a new project from files, sets related app state, and logs the status.
   *
   * @param project - The project to create.
   * @param files - The files to upload.
   * @param callbacks - The callbacks to use on success, error, and complete.
   */
  async function handleBulkImport(
    project: Pick<
      ProjectSchema,
      "projectId" | "name" | "description" | "projectVersion"
    >,
    files: File[],
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await createProjectApi.handleRequest(
      async () => {
        const formData = new FormData();

        formData.append("name", project.name);
        formData.append("description", project.description);

        files.forEach((file: File) => {
          formData.append("files", file);
        });

        const job = await createProjectUploadJob(formData);

        await jobApiStore.handleCreate(job);
      },
      {
        ...callbacks,
        onComplete: async () => {
          await navigateTo(Routes.UPLOAD_STATUS);
          callbacks.onSuccess?.();
        },
      },
      {
        useAppLoad: true,
        success: `Project has been created: ${project.name}`,
        error: `Unable to create project: ${project.name}`,
      }
    );
  }

  /**
   * Imports a Jira project, sets related app state, and moves to the upload page.
   *
   * @param onSuccess - Called if the action is successful.
   * @param onError - Called if the action fails.
   */
  async function handleJiraImport({
    onSuccess,
    onError,
  }: IOHandlerCallback): Promise<void> {
    const installationId = integrationsStore.jiraOrganization?.id;
    const projectId = integrationsStore.jiraProject?.id;

    if (!installationId || !projectId) return;

    await createProjectApi.handleRequest(
      () => createJiraProject(installationId, projectId),
      {
        onSuccess: async (job) => {
          integrationsStore.jiraProject = undefined;

          await jobApiStore.handleCreate(job);
          await navigateTo(Routes.UPLOAD_STATUS);

          onSuccess?.();
        },
        onError,
      },
      {
        useAppLoad: true,
        success: `Jira project has been created: ${projectId}`,
        error: `Unable to import jira project: ${projectId}`,
      }
    );
  }

  /**
   * Imports a GitHub project, sets related app state, and moves to the upload page.
   *
   * @param onSuccess - Called if the action is successful.
   * @param onError - Called if the action fails.
   */
  async function handleGitHubImport({
    onSuccess,
    onError,
  }: IOHandlerCallback): Promise<void> {
    const repositoryName = integrationsStore.gitHubProject?.name;
    const owner = integrationsStore.gitHubProject?.owner;

    if (!repositoryName || !owner) return;

    await createProjectApi.handleRequest(
      () =>
        createGitHubProject(
          owner,
          repositoryName,
          integrationsStore.gitHubConfig
        ),
      {
        onSuccess: async (job) => {
          integrationsStore.gitHubProject = undefined;

          await jobApiStore.handleCreate(job);
          await navigateTo(Routes.UPLOAD_STATUS);

          onSuccess?.();
        },
        onError,
      },
      {
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
});

export default useCreateProjectApi(pinia);
