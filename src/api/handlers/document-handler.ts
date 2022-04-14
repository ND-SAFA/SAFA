import { Artifact, DocumentType, ProjectDocument } from "@/types";
import { createDocument } from "@/util";
import { documentModule, projectModule } from "@/store";
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
