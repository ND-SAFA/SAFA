import { defineStore } from "pinia";

import { computed } from "vue";
import {
  DocumentType,
  IOHandlerCallback,
  DocumentSchema,
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
  saveDocument,
  deleteDocument,
  getDocuments,
  setCurrentDocument,
  clearCurrentDocument,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing document API requests.
 */
const useDocumentApi = defineStore("documentApi", (): DocumentApiHook => {
  const documentApi = useApi("documentApi");

  const loading = computed(() => documentApi.loading);

  async function handleCreate(
    name: string,
    type: DocumentType,
    artifactIds: string[]
  ): Promise<void> {
    await documentApi.handleRequest(async () => {
      const versionId = projectStore.versionIdWithLog;
      const createdDocument = await saveDocument(
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

      await setCurrentDocument(createdDocument.documentId);
      await documentStore.addDocument(createdDocument);
    });
  }

  async function handleCreatePreset(
    document: DocumentSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const { name, type, artifactIds } = document;

    await documentApi.handleRequest(
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

  async function handleUpdate(document: DocumentSchema): Promise<void> {
    await documentApi.handleRequest(async () => {
      const versionId = projectStore.versionIdWithLog;
      const updatedDocument = await saveDocument(versionId, document);

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

        await documentApi.handleRequest(
          async () => {
            await deleteDocument(document.documentId);
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
    await documentApi.handleRequest(async () => {
      const documents = await getDocuments(versionId);

      await documentStore.updateDocuments(documents);

      documentStore.baseDocument.artifactIds = artifacts.map(({ id }) => id);
    });
  }

  async function handleSave(callbacks: IOHandlerCallback): Promise<void> {
    const document = documentSaveStore.finalizedDocument;
    const isUpdate = documentSaveStore.isUpdate;
    const { name, type, artifactIds } = document;

    await documentApi.handleRequest(
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

  async function handleSwitch(document: DocumentSchema): Promise<void> {
    await documentApi.handleRequest(async () => {
      await documentStore.switchDocuments(document);

      if (document.documentId) {
        await setCurrentDocument(document.documentId);
      } else {
        await clearCurrentDocument();
      }
    });
  }

  return {
    loading,
    handleCreate,
    handleCreatePreset,
    handleUpdate,
    handleDelete,
    handleReload,
    handleSave,
    handleSwitch,
  };
});

export default useDocumentApi(pinia);
