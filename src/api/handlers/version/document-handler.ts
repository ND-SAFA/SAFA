import {
  ColumnModel,
  DocumentType,
  IOHandlerCallback,
  DocumentModel,
} from "@/types";
import { createDocument } from "@/util";
import { logStore, documentStore, projectStore } from "@/hooks";
import {
  saveDocument,
  deleteDocument,
  getDocuments,
  setCurrentDocument,
  clearCurrentDocument,
} from "@/api";

/**
 * Creates a new document and updates app state.
 *
 * @param name - The document name create.
 * @param type - The document type create.
 * @param artifactIds - The artifacts shown in the document.
 */
export async function handleCreateDocument(
  name: string,
  type: DocumentType,
  artifactIds: string[]
): Promise<void> {
  const versionId = projectStore.versionIdWithLog;
  const createdDocument = await saveDocument(
    versionId,
    createDocument({
      project: projectStore.project,
      artifactIds,
      name,
      type,
    })
  );

  await setCurrentDocument(createdDocument.documentId);
  await documentStore.addDocument(createdDocument);
}

/**
 * Updates an existing document and updates app state.
 *
 * @param document - The document to edit.
 */
export async function handleUpdateDocument(
  document: DocumentModel
): Promise<void> {
  const versionId = projectStore.versionIdWithLog;
  const updatedDocument = await saveDocument(versionId, document);

  await documentStore.updateDocuments([updatedDocument]);
}

/**
 * Deletes the document and updates app state.
 * Switches documents if the current one has been deleted.
 *
 * @param document - The document to delete.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleDeleteDocument(
  document: DocumentModel,
  { onSuccess, onError }: IOHandlerCallback
): void {
  const { name } = document;

  deleteDocument(document)
    .then(async () => {
      await documentStore.removeDocument(document);
      logStore.onSuccess(`Document has been deleted: ${name}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to delete document: ${name}`);
      logStore.onDevError(e);
      onError?.(e);
    });
}

/**
 * Updates the artifact for the all documents.
 *
 * @param versionId - The project version to load documents for.
 * @param artifacts - The full list of artifacts.
 */
export async function handleDocumentReload(
  versionId = projectStore.versionId,
  artifacts = projectStore.project.artifacts
): Promise<void> {
  const documents = await getDocuments(versionId);

  await documentStore.updateDocuments(documents);

  documentStore.baseDocument.artifactIds = artifacts.map(({ id }) => id);
}

/**
 * Creates or updates a document, updates app state, and logs the result.
 *
 * @param document - The document to save.
 * @param isUpdate - Set to true if the document already exists.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleSaveDocument(
  document: DocumentModel,
  isUpdate: boolean,
  { onSuccess, onError }: IOHandlerCallback
): void {
  const { name, type, artifactIds } = document;

  if (isUpdate) {
    handleUpdateDocument(document)
      .then(() => {
        logStore.onSuccess(`Document has been edited: ${name}`);
        onSuccess?.();
      })
      .catch((e) => {
        logStore.onError(`Unable to edit document: ${name}`);
        logStore.onDevError(e);
        onError?.(e);
      });
  } else {
    handleCreateDocument(name, type, artifactIds)
      .then(() => {
        logStore.onSuccess(`Document has been created: ${name}`);
        onSuccess?.();
      })
      .catch((e) => {
        logStore.onError(`Unable to create document: ${name}`);
        logStore.onDevError(e);
        onError?.(e);
      });
  }
}

/**
 * Changes the order of two columns.
 *
 * @param column - The column to move.
 * @param moveUp - Whether to move the column up or down.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleColumnMove(
  column: ColumnModel,
  moveUp: boolean,
  { onSuccess, onError }: IOHandlerCallback<ColumnModel[]>
): void {
  const document = documentStore.currentDocument;
  const currentIndex = (document.columns || []).indexOf(column);
  const swapIndex = moveUp ? currentIndex - 1 : currentIndex + 1;
  const columns = document.columns || [];

  [columns[currentIndex], columns[swapIndex]] = [
    columns[swapIndex],
    columns[currentIndex],
  ];

  document.columns = [...columns];

  handleUpdateDocument(document)
    .then(() => {
      logStore.onSuccess(`Column order has been updated.`);
      onSuccess?.(document.columns || []);
    })
    .catch((e) => {
      logStore.onError(`Unable to update column order.`);
      logStore.onDevError(e);
      onError?.(e);
    });
}

/**
 * Creates or updates a column.
 *
 * @param column - The column to save.
 * @param isEditMode - If false, this column will be added to the current document.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleColumnSave(
  column: ColumnModel,
  isEditMode: boolean,
  { onSuccess, onError }: IOHandlerCallback
): void {
  const document = documentStore.currentDocument;
  const { id: columnId, name } = column;

  if (!isEditMode) {
    document.columns = [...(document.columns || []), column];
  } else if (document.columns) {
    const index = document.columns.findIndex(({ id }) => id === columnId);

    document.columns[index] = column;
  }

  handleUpdateDocument(document)
    .then(() => {
      logStore.onSuccess(`Column has been updated: ${name}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to update column: ${name}`);
      logStore.onDevError(e);
      onError?.(e);
    });
}

/**
 * Deletes a column.
 *
 * @param column - The column to delete.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleColumnDelete(
  column: ColumnModel,
  { onSuccess, onError }: IOHandlerCallback
): void {
  const document = documentStore.currentDocument;
  const { id: columnId, name } = column;

  document.columns = (document.columns || []).filter(
    ({ id }) => id !== columnId
  );

  handleUpdateDocument(document)
    .then(() => {
      logStore.onSuccess(`Column has ben deleted: ${name}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable to delete column: ${name}`);
      logStore.onDevError(e);
      onError?.(e);
    });
}

/**
 * Switches documents and updates the currently saved document.
 *
 * @param document - The current document.
 */
export async function handleSwitchDocuments(
  document: DocumentModel
): Promise<void> {
  documentStore.switchDocuments(document);

  if (document.documentId) {
    await setCurrentDocument(document.documentId);
  } else {
    await clearCurrentDocument();
  }
}
