import { defineStore } from "pinia";
import { computed } from "vue";
import { saveAs } from "file-saver";

import {
  IOHandlerCallback,
  ProjectApiHook,
  ProjectSchema,
  TransferProjectSchema,
} from "@/types";
import { versionToString } from "@/util";
import {
  getProjectApiStore,
  identifierSaveStore,
  projectStore,
  setProjectApiStore,
  useApi,
} from "@/hooks";
import {
  deleteProject,
  getProjectFiles,
  createProject,
  editProject,
  setProjectOwner,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing project API requests.
 */
export const useProjectApi = defineStore("projectApi", (): ProjectApiHook => {
  const saveProjectApi = useApi("saveProjectApi");
  const deleteProjectApi = useApi("deleteProjectApi");

  const saveProjectLoading = computed(() => saveProjectApi.loading);
  const deleteProjectLoading = computed(() => deleteProjectApi.loading);

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

  async function handleDelete(callbacks: IOHandlerCallback): Promise<void> {
    const project = identifierSaveStore.baseIdentifier;

    if (!project) return;

    await deleteProjectApi.handleRequest(
      async () => {
        await deleteProject(project.projectId);

        projectStore.removeProject(project, () =>
          setProjectApiStore.handleClear()
        );

        await getProjectApiStore.handleLoadProjects();
      },
      {
        ...callbacks,
        success: `Project has been deleted: ${project.name}`,
        error: `Unable to delete project: ${project.name}`,
      }
    );
  }

  async function handleTransfer(
    newOwner: TransferProjectSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const project = identifierSaveStore.baseIdentifier;

    if (!project) return;

    await saveProjectApi.handleRequest(
      async () => {
        const updatedIdentifier = await setProjectOwner(
          project.projectId,
          newOwner
        );

        projectStore.updateProject(updatedIdentifier);
      },
      {
        ...callbacks,
        success: `Project has been transferred: ${project.name}`,
        error: `Unable to transferred project: ${project.name}`,
      }
    );
  }

  return {
    saveProjectLoading,
    deleteProjectLoading,
    handleSave,
    handleDownload,
    handleDelete,
    handleTransfer,
  };
});

export default useProjectApi(pinia);
