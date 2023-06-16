import { defineStore } from "pinia";

import { ProjectSchema } from "@/types";
import { createProject } from "@/util";
import {
  deltaStore,
  documentStore,
  getVersionApiStore,
  integrationsApiStore,
  notificationApiStore,
  projectStore,
  subtreeStore,
  useApi,
} from "@/hooks";
import { QueryParams, removeParams, updateParam } from "@/router";
import { getProjectArtifactTypes, getTraceMatrices } from "@/api";
import { pinia } from "@/plugins";

export const useSetProjectApi = defineStore("setProjectApi", () => {
  const setProjectApi = useApi("setProjectApi");

  /**
   * Moves user to the document if one is set by currentDocumentId.
   * Otherwise default document would continue to be in view.
   *
   * @param project The project possibly containing a currentDocumentId.
   */
  async function setCurrentDocument(project: ProjectSchema): Promise<void> {
    if (!project.currentDocumentId) return;

    const document = project.documents.find(
      (d) => d.documentId === project.currentDocumentId
    );

    if (!document) return;

    await documentStore.switchDocuments(document);
  }

  /**
   * Clears project store data.
   */
  async function handleClear(): Promise<void> {
    const project = createProject();

    projectStore.initializeProject(project);
    subtreeStore.$reset();
    await removeParams();
  }

  /**
   * Sets a newly created project.
   *
   * @param project - Project created containing entities.
   */
  async function handleSet(project: ProjectSchema): Promise<void> {
    await setProjectApi.handleRequest(async () => {
      const projectId = project.projectId;
      const versionId = project.projectVersion?.versionId || "";

      project.artifactTypes = await getProjectArtifactTypes(projectId);
      project.typeDirections = await getTraceMatrices(projectId);
      projectStore.initializeProject(project);

      await notificationApiStore.handleSubscribeVersion(projectId, versionId);
      await integrationsApiStore.handleReload();
      await setCurrentDocument(project);
      await updateParam(QueryParams.VERSION, versionId);
    });
  }

  /**
   * Reloads the current project.
   */
  async function handleReload(): Promise<void> {
    deltaStore.setIsDeltaViewEnabled(false);
    await getVersionApiStore.handleLoad(
      projectStore.versionId,
      documentStore.currentDocument
    );
  }

  return { handleClear, handleSet, handleReload };
});

export default useSetProjectApi(pinia);
