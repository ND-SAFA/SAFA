import { documentModule, projectModule } from "@/store";
import { Artifact, DocumentType, Project, ProjectDocument } from "@/types";
import {
  saveDocument,
  deleteDocument,
  getDocuments,
} from "@/api/endpoints/document-api";
import { createDocument } from "@/util";

/**
 * Adds documents to the given project object.
 *
 * @param project - The project to load documents for.
 */
export async function loadProjectDocuments(
  project: Project = projectModule.getProject
): Promise<void> {
  project.documents = await getDocuments(project.projectId).catch(() => []);
}

/**
 * Creates a new document.
 *
 * @param name - The document name create.
 * @param type - The document type create.
 * @param artifactIds - The artifacts shown in the document.
 */
export async function addNewDocument(
  name: string,
  type: DocumentType,
  artifactIds: string[]
): Promise<void> {
  const versionId = projectModule.versionIdWithLog;

  if (!versionId) return;

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
 * Edits an existing document.
 *
 * @param document - The document to edit.
 */
export async function editDocument(document: ProjectDocument): Promise<void> {
  const versionId = projectModule.versionIdWithLog;

  if (!versionId) return;

  const updatedDocument = await saveDocument(versionId, document);
  await documentModule.updateDocuments([updatedDocument]);

  if (documentModule.document.documentId === updatedDocument.documentId) {
    await documentModule.switchDocuments(updatedDocument);
  }
}

/**
 * Deletes the document and switches document's if this one was visible.
 *
 * @param document - The document to delete.
 */
export async function deleteAndSwitchDocuments(
  document: ProjectDocument
): Promise<void> {
  await deleteDocument(document);
  await documentModule.removeDocument(document);
}

/**
 * Updates the artifact IDs for the all documents.
 *
 * @param projectId - The project to load documents for.
 * @param artifacts - The full list of artifacts.
 */
export async function reloadDocumentArtifacts(
  projectId = projectModule.projectId,
  artifacts: Artifact[] = projectModule.getProject.artifacts
): Promise<void> {
  const documents = await getDocuments(projectId);

  await documentModule.updateDocuments(documents);

  documentModule.defaultDocument.artifactIds = artifacts.map(({ id }) => id);
}
