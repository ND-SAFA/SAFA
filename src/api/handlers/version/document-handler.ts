import {
  ColumnModel,
  DocumentType,
  IOHandlerCallback,
  DocumentModel,
} from "@/types";
import { createDocument, preserveObjectKeys } from "@/util";
import {
  logStore,
  documentStore,
  projectStore,
  appStore,
  tableColumnSaveStore,
  documentSaveStore,
} from "@/hooks";
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
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleDeleteDocument({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const document = documentSaveStore.editedDocument;
  const { name } = document;

  logStore.confirm(
    "Delete Document",
    `Are you sure you want to delete the document "${name}"?`,
    async (confirmed) => {
      if (!confirmed) return;

      await deleteDocument(document)
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
  );
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
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleSaveDocument({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const document = documentSaveStore.finalizedDocument;
  const isUpdate = documentSaveStore.isUpdate;
  const { name, type, artifactIds } = document;

  appStore.onLoadStart();

  const handleSuccess = (isNew: boolean) => () => {
    logStore.onSuccess(
      isNew
        ? `Document has been created: ${name}`
        : `Document has been edited: ${name}`
    );
    onSuccess?.();
    appStore.onLoadEnd();
  };

  const handleError = (isNew: boolean) => (e: Error) => {
    logStore.onError(
      isNew
        ? `Unable to create document: ${name}`
        : `Unable to edit document: ${name}`
    );
    logStore.onDevError(String(e));
    onError?.(e);
    appStore.onLoadEnd();
  };

  if (isUpdate) {
    handleUpdateDocument(document)
      .then(handleSuccess(false))
      .catch(handleError(false));
  } else {
    handleCreateDocument(name, type, artifactIds)
      .then(handleSuccess(true))
      .catch(handleError(true));
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
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleColumnSave({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const column = tableColumnSaveStore.editedColumn;
  const isUpdate = tableColumnSaveStore.isUpdate;
  const document = documentStore.currentDocument;
  const { id: columnId, name } = column;

  if (!isUpdate) {
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
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleColumnDelete({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const column = tableColumnSaveStore.editedColumn;
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
