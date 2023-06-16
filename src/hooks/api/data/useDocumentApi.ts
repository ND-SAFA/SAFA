import { defineStore } from "pinia";

import { DocumentType, IOHandlerCallback, DocumentSchema } from "@/types";
import { createDocument, preserveObjectKeys } from "@/util";
import {
  useApi,
  logStore,
  documentStore,
  projectStore,
  documentSaveStore,
} from "@/hooks";
import {
  saveDocument,
  deleteDocument,
  getDocuments,
  setCurrentDocument,
  clearCurrentDocument,
} from "@/api";
import { pinia } from "@/plugins";

const useDocumentApi = defineStore("documentApi", () => {
  const documentApi = useApi("documentApi");

  /**
   * Creates a new document and updates app state.
   *
   * @param name - The document name create.
   * @param type - The document type create.
   * @param artifactIds - The artifacts shown in the document.
   */
  async function handleCreateDocument(
    name: string,
    type: DocumentType,
    artifactIds: string[]
  ): Promise<void> {
    await documentApi.handleRequest(async () => {
      const versionId = projectStore.versionIdWithLog;
      const createdDocument = await saveDocument(
        versionId,
        createDocument({
          project: preserveObjectKeys(projectStore.project, [
            "name",
            "description",
            "projectId",
            "members",
            "owner",
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

  /**
   * Creates a new document from an existing document and updates app state.
   *
   * @param document - The document to create.
   * @param callbacks - The callbacks to call on success, error, and complete.
   */
  async function handleCreatePresetDocument(
    document: DocumentSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const { name, type, artifactIds } = document;

    await documentApi.handleRequest(
      async () => {
        await documentStore.removeDocument(document);
        await handleCreateDocument(name, type, artifactIds);
      },
      callbacks,
      {
        useAppLoad: true,
        success: `Document has been created: ${name}`,
        error: `Cannot create document: ${name}`,
      }
    );
  }

  /**
   * Updates an existing document and updates app state.
   *
   * @param document - The document to edit.
   */
  async function handleUpdateDocument(document: DocumentSchema): Promise<void> {
    await documentApi.handleRequest(async () => {
      const versionId = projectStore.versionIdWithLog;
      const updatedDocument = await saveDocument(versionId, document);

      await documentStore.updateDocuments([updatedDocument]);
    });
  }

  /**
   * Deletes the document and updates app state.
   * Switches documents if the current one has been deleted.
   *
   * @param callbacks - The callbacks to call on success, error, and complete.
   */
  function handleDeleteDocument(callbacks: IOHandlerCallback): void {
    const document = documentSaveStore.editedDocument;
    const { name } = document;

    logStore.confirm(
      "Delete Document",
      `Are you sure you want to delete the document "${name}"?`,
      async (confirmed) => {
        if (!confirmed) return;

        await documentApi.handleRequest(
          async () => {
            await deleteDocument(document);
            await documentStore.removeDocument(document);
          },
          callbacks,
          {
            useAppLoad: true,
            success: `Document has been deleted: ${name}`,
            error: `Unable to delete document: ${name}`,
          }
        );
      }
    );
  }

  /**
   * Updates the artifact for the all documents.
   *
   * @param versionId - The project version to load documents for.
   * @param artifacts - The full list of artifacts.
   */
  async function handleReloadDocuments(
    versionId = projectStore.versionId,
    artifacts = projectStore.project.artifacts
  ): Promise<void> {
    await documentApi.handleRequest(async () => {
      const documents = await getDocuments(versionId);

      await documentStore.updateDocuments(documents);

      documentStore.baseDocument.artifactIds = artifacts.map(({ id }) => id);
    });
  }

  /**
   * Creates or updates a document, updates app state, and logs the result.
   *
   * @param callbacks - The callbacks to call on success, error, and complete.
   */
  async function handleSaveDocument(
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const document = documentSaveStore.finalizedDocument;
    const isUpdate = documentSaveStore.isUpdate;
    const { name, type, artifactIds } = document;

    await documentApi.handleRequest(
      async () =>
        isUpdate
          ? handleUpdateDocument(document)
          : handleCreateDocument(name, type, artifactIds),
      callbacks,
      {
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

  /**
   * Switches documents and updates the currently saved document.
   *
   * @param document - The current document.
   */
  async function handleSwitchDocuments(
    document: DocumentSchema
  ): Promise<void> {
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
    handleCreateDocument,
    handleCreatePresetDocument,
    handleUpdateDocument,
    handleDeleteDocument,
    handleReloadDocuments,
    handleSaveDocument,
    handleSwitchDocuments,
  };
});

export default useDocumentApi(pinia);
