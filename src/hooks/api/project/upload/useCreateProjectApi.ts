import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, ProjectSchema } from "@/types";
import {
  integrationsStore,
  jobApiStore,
  logStore,
  projectSaveStore,
  projectStore,
} from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  createGitHubProject,
  createJiraProject,
  createProjectCreationJob,
  handleLoadVersion,
  handleUploadProjectVersion,
  saveProject,
} from "@/api";
import { pinia } from "@/plugins";
import { useApi } from "@/hooks/api/useApi";

export const useCreateProjectApi = defineStore("createProjectApi", () => {
  const createProjectApi = useApi("createProjectApi")();

  const loading = computed(() => createProjectApi.loading);

  /**
   * Creates a new project, sets related app state, and logs the status.
   *
   * @param onSuccess - Called if the action is successful.
   * @param onError - Called if the action fails.
   */
  async function handleImportProject({
    onSuccess,
    onError,
  }: IOHandlerCallback): Promise<void> {
    const projectCreationRequest = projectSaveStore.creationRequest;
    const name = projectCreationRequest.project.name;

    await createProjectApi.handleRequest(
      async () => createProjectCreationJob(projectCreationRequest),
      {
        onSuccess: async (job) => {
          await jobApiStore.handleCreateJob(job);
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
   * @param onSuccess - Called if the action is successful.
   * @param onError - Called if the action fails.
   */
  async function handleBulkImportProject(
    project: Pick<
      ProjectSchema,
      "projectId" | "name" | "description" | "projectVersion"
    >,
    files: File[],
    { onSuccess, onError }: IOHandlerCallback
  ): Promise<void> {
    await createProjectApi.handleRequest(
      () => saveProject(project),
      {
        onSuccess: async (project) => {
          if (files.length === 0) {
            logStore.onSuccess(`Project has been created: ${project.name}`);
            projectStore.addProject(project);

            await handleLoadVersion(project.projectVersion?.versionId || "");
          } else {
            await handleUploadProjectVersion(
              project.projectId,
              project.projectVersion?.versionId || "",
              files,
              true
            );
          }
          onSuccess?.();
        },
        onError,
      },
      { useAppLoad: true }
    );
  }

  /**
   * Imports a Jira project, sets related app state, and moves to the upload page.
   *
   * @param onSuccess - Called if the action is successful.
   * @param onError - Called if the action fails.
   */
  async function handleImportJiraProject({
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

          await jobApiStore.handleCreateJob(job);
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
  async function handleImportGitHubProject({
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

          await jobApiStore.handleCreateJob(job);
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
    handleImportProject,
    handleBulkImportProject,
    handleImportJiraProject,
    handleImportGitHubProject,
  };
});

export default useCreateProjectApi(pinia);
