import { defineStore } from "pinia";

import { computed } from "vue";
import {
  ViewType,
  IOHandlerCallback,
  ViewSchema,
  DocumentApiHook,
} from "@/types";
import { buildDocument, preserveObjectKeys } from "@/util";
import {
  useApi,
  logStore,
  documentStore,
  projectStore,
  documentSaveStore,
  artifactStore,
} from "@/hooks";
import {
  saveView,
  deleteView,
  getViews,
  setCurrentView,
  clearCurrentView,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing view API requests.
 */
const useViewApi = defineStore("documentApi", (): DocumentApiHook => {
  const viewApi = useApi("viewApi");

  const loading = computed(() => viewApi.loading);

  const currentDocument = computed({
    get() {
      return documentStore.currentDocument;
    },
    set(document) {
      handleSwitch(document);
    },
  });

  async function handleCreate(
    name: string,
    type: ViewType,
    artifactIds: string[]
  ): Promise<void> {
    await viewApi.handleRequest(async () => {
      const versionId = projectStore.versionIdWithLog;
      const createdDocument = await saveView(
        versionId,
        buildDocument({
          project: preserveObjectKeys(projectStore.project, [
            "name",
            "description",
            "projectId",
            "members",
            "owner",
            "orgId",
            "teamId",
            "permissions",
          ]),
          artifactIds,
          name,
          type,
        })
      );

      await setCurrentView(createdDocument.documentId);
      await documentStore.addDocument(createdDocument);
    });
  }

  async function handleCreatePreset(
    document: ViewSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const { name, type, artifactIds } = document;

    await viewApi.handleRequest(
      async () => {
        await documentStore.removeDocument(document);
        await handleCreate(name, type, artifactIds);
      },
      {
        ...callbacks,
        useAppLoad: true,
        success: `Document has been created: ${name}`,
        error: `Cannot create document: ${name}`,
      }
    );
  }

  async function handleUpdate(document: ViewSchema): Promise<void> {
    await viewApi.handleRequest(async () => {
      const versionId = projectStore.versionIdWithLog;
      const updatedDocument = await saveView(versionId, document);

      await documentStore.updateDocuments([updatedDocument]);
    });
  }

  function handleDelete(callbacks: IOHandlerCallback): void {
    const document = documentSaveStore.editedDocument;
    const { name } = document;

    logStore.confirm(
      "Delete Document",
      `Are you sure you want to delete the document "${name}"?`,
      async (confirmed) => {
        if (!confirmed) return;

        await viewApi.handleRequest(
          async () => {
            await deleteView(document.documentId);
            await documentStore.removeDocument(document);
          },
          {
            ...callbacks,
            useAppLoad: true,
            success: `Document has been deleted: ${name}`,
            error: `Unable to delete document: ${name}`,
          }
        );
      }
    );
  }

  async function handleReload(
    versionId = projectStore.versionId,
    artifacts = artifactStore.allArtifacts
  ): Promise<void> {
    await viewApi.handleRequest(async () => {
      const documents = await getViews(versionId);

      await documentStore.updateDocuments(documents);

      documentStore.baseDocument.artifactIds = artifacts.map(({ id }) => id);
    });
  }

  async function handleSave(callbacks: IOHandlerCallback): Promise<void> {
    const document = documentSaveStore.finalizedDocument;
    const isUpdate = documentSaveStore.isUpdate;
    const { name, type, artifactIds } = document;

    await viewApi.handleRequest(
      async () =>
        isUpdate
          ? handleUpdate(document)
          : handleCreate(name, type, artifactIds),
      {
        ...callbacks,
        useAppLoad: true,
        success: isUpdate
          ? `Document has been edited: ${name}`
          : `Document has been created: ${name}`,
        error: isUpdate
          ? `Unable to edit document: ${name}`
          : `Unable to create document: ${name}`,
      }
    );
  }

  async function handleSwitch(document: ViewSchema): Promise<void> {
    await viewApi.handleRequest(async () => {
      await documentStore.switchDocuments(document);

      if (document.documentId) {
        await setCurrentView(document.documentId);
      } else {
        await clearCurrentView();
      }
    });
  }

  return {
    loading,
    currentDocument,
    handleCreate,
    handleCreatePreset,
    handleUpdate,
    handleDelete,
    handleReload,
    handleSave,
    handleSwitch,
  };
});

export default useViewApi(pinia);
