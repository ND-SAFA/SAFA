import {
  Artifact,
  DocumentColumn,
  DocumentType,
  ProjectDocument,
} from "@/types";
import { createDocument } from "@/util";
import { documentModule, logModule, projectModule } from "@/store";
import { saveDocument, deleteDocument, getDocuments } from "@/api";

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
  const versionId = projectModule.versionIdWithLog;
  const createdDocument = await saveDocument(
    versionId,
    createDocument({
      project: projectModule.getProject,
      artifactIds,
      name,
      type,
    })
  );

  await documentModule.addDocument(createdDocument);
}

/**
 * Updates an existing document and updates app state.
 *
 * @param document - The document to edit.
 */
export async function handleUpdateDocument(
  document: ProjectDocument
): Promise<void> {
  const versionId = projectModule.versionIdWithLog;
  const updatedDocument = await saveDocument(versionId, document);

  await documentModule.updateDocuments([updatedDocument]);

  if (documentModule.document.documentId === updatedDocument.documentId) {
    await documentModule.switchDocuments(updatedDocument);
  }
}

/**
 * Deletes the document and updates app state.
 * Switches documents if the current one has been deleted.
 *
 * @param document - The document to delete.
 */
export async function handleDeleteDocument(
  document: ProjectDocument
): Promise<void> {
  await deleteDocument(document);
  await documentModule.removeDocument(document);
}

/**
 * Updates the artifact for the all documents.
 *
 * @param projectId - The project to load documents for.
 * @param artifacts - The full list of artifacts.
 */
export async function handleDocumentReload(
  projectId = projectModule.projectId,
  artifacts: Artifact[] = projectModule.getProject.artifacts
): Promise<void> {
  const documents = await getDocuments(projectId);

  await documentModule.updateDocuments(documents);

  documentModule.defaultDocument.artifactIds = artifacts.map(({ id }) => id);
}

/**
 * Changes the order of two columns.
 *
 * @param column - The column to move.
 * @param moveUp - Whether to move the column up or down.
 * @param onSuccess - Called if the operation is successful.
 */
export function handleColumnMove(
  column: DocumentColumn,
  moveUp: boolean,
  onSuccess: (cols: DocumentColumn[]) => void
): void {
  const document = documentModule.document;
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
      logModule.onSuccess(`Column order updated`);
      onSuccess(document.columns || []);
    })
    .catch(() => logModule.onError(`Unable to update column order`));
}

/**
 * Creates or updates a column.
 *
 * @param column - The column to save.
 * @param isEditMode - If false, this column will be added to the current document.
 * @param onSuccess - Called if the operation is successful.
 */
export function handleColumnSave(
  column: DocumentColumn,
  isEditMode: boolean,
  onSuccess: () => void
): void {
  const document = documentModule.document;
  const { id: columnId, name } = column;

  if (!isEditMode) {
    document.columns = [...(document.columns || []), column];
  } else if (document.columns) {
    const index = document.columns.findIndex(({ id }) => id === columnId);

    document.columns[index] = column;
  }

  handleUpdateDocument(document)
    .then(() => {
      logModule.onSuccess(`Column updated: ${name}`);
      onSuccess();
    })
    .catch(() => logModule.onError(`Unable to update column: ${name}`));
}

/**
 * Deletes a column.
 *
 * @param column - The column to delete.
 * @param onSuccess - Called if the operation is successful.
 */
export function handleColumnDelete(
  column: DocumentColumn,
  onSuccess: () => void
): void {
  const document = documentModule.document;
  const { id: columnId, name } = column;

  document.columns = (document.columns || []).filter(
    ({ id }) => id !== columnId
  );

  handleUpdateDocument(document)
    .then(() => {
      logModule.onSuccess(`Column deleted: ${name}`);
      onSuccess();
    })
    .catch(() => logModule.onError(`Unable to delete column: ${name}`));
}
