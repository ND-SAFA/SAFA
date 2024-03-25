import { defineStore } from "pinia";

import { ProjectSchema, SetProjectApiHook } from "@/types";
import { buildProject } from "@/util";
import {
  documentStore,
  integrationsApiStore,
  projectStore,
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
      await removeParams();
    }

    async function handleSet(project: ProjectSchema): Promise<void> {
      await setProjectApi.handleRequest(async () => {
        projectStore.initializeProject(project);

        await handleSetCurrentDocument(project);
        await updateParam(QueryParams.VERSION, projectStore.versionId);
        await integrationsApiStore.handleLoadInstallations();
      });
    }

    return { handleClear, handleSet };
  }
);

export default useSetProjectApi(pinia);
