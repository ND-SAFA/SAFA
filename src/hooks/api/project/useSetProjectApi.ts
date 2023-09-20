import { defineStore } from "pinia";

import { ProjectSchema, SetProjectApiHook } from "@/types";
import { buildProject } from "@/util";
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
import { pinia } from "@/plugins";

/**
 * A hook for managing set project API requests.
 */
export const useSetProjectApi = defineStore(
  "setProjectApi",
  (): SetProjectApiHook => {
    const setProjectApi = useApi("setProjectApi");

    async function handleSetCurrentDocument(
      project: ProjectSchema
    ): Promise<void> {
      if (!project.currentDocumentId) return;

      const document = project.documents.find(
        (d) => d.documentId === project.currentDocumentId
      );

      if (!document) return;

      await documentStore.switchDocuments(document);
    }

    async function handleClear(): Promise<void> {
      const project = buildProject();

      projectStore.initializeProject(project);
      subtreeStore.$reset();
      await removeParams();
    }

    async function handleSet(project: ProjectSchema): Promise<void> {
      await setProjectApi.handleRequest(async () => {
        const projectId = project.projectId;
        const versionId = project.projectVersion?.versionId || "";

        projectStore.initializeProject(project);

        await notificationApiStore.handleSubscribeVersion(projectId, versionId);
        await integrationsApiStore.handleReload();
        await handleSetCurrentDocument(project);
        await updateParam(QueryParams.VERSION, versionId);
      });
    }

    async function handleReload(): Promise<void> {
      deltaStore.setIsDeltaViewEnabled(false);
      await getVersionApiStore.handleLoad(
        projectStore.versionId,
        documentStore.currentDocument
      );
    }

    return { handleSetCurrentDocument, handleClear, handleSet, handleReload };
  }
);

export default useSetProjectApi(pinia);
