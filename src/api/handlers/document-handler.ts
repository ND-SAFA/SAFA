import { documentModule, projectModule } from "@/store";
import { Project, ProjectDocument } from "@/types";
import {
  createOrUpdateDocument,
  deleteDocument,
  getProjectDocuments,
} from "@/api/endpoints/document-api";
import { createDocument } from "@/util";

/**
 * Adds documents to the given project object.
 *
 * @param project - The project to load documents for.
 */
export async function loadProjectDocuments(project: Project): Promise<void> {
  project.documents = await getProjectDocuments(project.projectId).catch(
    () => []
  );
}

/**
 * Creates a new document.
 *
 * @param documentName - The document name create.
 * @param artifactIds - The artifacts shown in the document.
 */
export async function addNewDocument(
  documentName: string,
  artifactIds: string[]
): Promise<void> {
  const createdDocument = await createOrUpdateDocument(
    projectModule.projectId,
    createDocument(projectModule.getProject, artifactIds, documentName)
  );

  documentModule.addDocument(createdDocument);
}

/**
 * Edits an existing document.
 *
 * @param document - The document to edit.
 */
export async function editDocument(document: ProjectDocument): Promise<void> {
  await createOrUpdateDocument(projectModule.projectId, document);

  if (documentModule.document === document) {
    await documentModule.switchDocuments(document);
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
