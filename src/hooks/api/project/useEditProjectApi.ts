import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, ProjectSchema, VersionSchema } from "@/types";
import { versionToString } from "@/util";
import {
  identifierSaveStore,
  logStore,
  projectStore,
  setProjectApiStore,
  useApi,
} from "@/hooks";
import { deleteProject, deleteProjectVersion, saveProject } from "@/api";
import { pinia } from "@/plugins";

export const useEditProjectApi = defineStore("editProjectApi", () => {
  const saveProjectApi = useApi("saveProjectApi");
  const deleteProjectApi = useApi("deleteProjectApi");
  const deleteVersionApi = useApi("deleteVersionApi");

  const saveProjectLoading = computed(() => saveProjectApi.loading);
  const deleteProjectLoading = computed(() => deleteProjectApi.loading);
  const deleteVersionLoading = computed(() => deleteVersionApi.loading);

  /**
   * Saves a project, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the action.
   */
  async function handleSaveProject(
    callbacks: IOHandlerCallback<ProjectSchema>
  ): Promise<void> {
    const identifier = identifierSaveStore.editedIdentifier;

    await saveProjectApi.handleRequest(
      async () => {
        const project = await saveProject(identifier);

        projectStore.addProject(identifier.projectId ? identifier : project);

        return project;
      },
      callbacks,
      {
        success: `Project has been saved: ${identifier.name}`,
        error: `Unable to save project: ${identifier.name}`,
      }
    );
  }

  /**
   * Deletes a project, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the action.
   */
  async function handleDeleteProject(
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const project = identifierSaveStore.baseIdentifier;

    if (!project) return;

    await deleteProjectApi.handleRequest(
      async () => {
        await deleteProject(project.projectId);

        projectStore.allProjects = projectStore.allProjects.filter(
          ({ projectId }) => projectId !== project.projectId
        );

        if (project.name !== projectStore.project.name) return;

        // Clear the current project if it has been deleted.
        await setProjectApiStore.handleClearProject();
      },
      callbacks,
      {
        success: `Project has been deleted: ${project.name}`,
        error: `Unable to delete project: ${project.name}`,
      }
    );
  }

  /**
   * Deletes a version, updates app state, and logs the status.
   *
   * @param version - The version to delete.
   * @param callbacks - Callbacks for the action.
   */
  function handleDeleteVersion(
    version: VersionSchema,
    callbacks: IOHandlerCallback
  ): void {
    const name = versionToString(version);

    logStore.confirm(
      `Delete Version`,
      `Are you sure you would like to delete "${name}"?`,
      async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        await deleteVersionApi.handleRequest(
          async () => deleteProjectVersion(version.versionId),
          callbacks,
          {
            success: `Version has been deleted: ${name}`,
            error: `Unable to delete version: ${name}`,
          }
        );
      }
    );
  }

  return {
    saveProjectLoading,
    deleteProjectLoading,
    deleteVersionLoading,
    handleSaveProject,
    handleDeleteProject,
    handleDeleteVersion,
  };
});

export default useEditProjectApi(pinia);
