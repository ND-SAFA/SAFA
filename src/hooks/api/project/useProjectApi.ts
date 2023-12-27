import { defineStore } from "pinia";
import { computed } from "vue";
import { saveAs } from "file-saver";

import {
  IOHandlerCallback,
  ProjectApiHook,
  ProjectSchema,
  VersionSchema,
} from "@/types";
import { versionToString } from "@/util";
import {
  identifierSaveStore,
  logStore,
  projectStore,
  setProjectApiStore,
  useApi,
} from "@/hooks";
import {
  deleteProject,
  deleteProjectVersion,
  getProjectFiles,
  createProject,
  editProject,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing project API requests.
 */
export const useProjectApi = defineStore("projectApi", (): ProjectApiHook => {
  const saveProjectApi = useApi("saveProjectApi");
  const deleteProjectApi = useApi("deleteProjectApi");
  const deleteVersionApi = useApi("deleteVersionApi");

  const saveProjectLoading = computed(() => saveProjectApi.loading);
  const deleteProjectLoading = computed(() => deleteProjectApi.loading);
  const deleteVersionLoading = computed(() => deleteVersionApi.loading);

  async function handleSave(
    callbacks: IOHandlerCallback<ProjectSchema> = {}
  ): Promise<void> {
    const identifier = identifierSaveStore.editedIdentifier;
    const isUpdate = identifierSaveStore.isUpdate;

    await saveProjectApi.handleRequest(
      async () => {
        const project = isUpdate
          ? await editProject(identifier)
          : await createProject(identifier);

        projectStore.addProject(isUpdate ? identifier : project);

        if (project.projectId === projectStore.projectId) {
          projectStore.updateProject({
            name: project.name,
            description: project.description,
          });
        }

        return project;
      },
      {
        ...callbacks,
        success: `Project has been saved: ${identifier.name}`,
        error: `Unable to save project: ${identifier.name}`,
      }
    );
  }

  async function handleDownload(
    fileType: "csv" | "json" = "csv"
  ): Promise<void> {
    await saveProjectApi.handleRequest(async () => {
      const data = await getProjectFiles(projectStore.versionId, fileType);

      const fileName = `${projectStore.project.name}-${versionToString(
        projectStore.version
      )}.zip`;
      const blob = new Blob([data], {
        type: "application/octet-stream",
      });

      saveAs(blob, fileName);
    });
  }

  async function handleDeleteProject(
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const project = identifierSaveStore.baseIdentifier;

    if (!project) return;

    await deleteProjectApi.handleRequest(
      async () => {
        await deleteProject(project.projectId);

        projectStore.removeProject(project);

        if (project.name !== projectStore.project.name) return;

        // Clear the current project if it has been deleted.
        await setProjectApiStore.handleClear();
      },
      {
        ...callbacks,
        success: `Project has been deleted: ${project.name}`,
        error: `Unable to delete project: ${project.name}`,
      }
    );
  }

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
          {
            ...callbacks,
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
    handleSave,
    handleDownload,
    handleDeleteProject,
    handleDeleteVersion,
  };
});

export default useProjectApi(pinia);
