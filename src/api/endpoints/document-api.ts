import { DocumentSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates or updates given document under project specified.
 *
 * @param versionId - The version to mark the document as created.
 * @param document - The document to be created.
 * @return The saved document.
 */
export async function saveDocument(
  versionId: string,
  document: DocumentSchema
): Promise<DocumentSchema> {
  return buildRequest<DocumentSchema, "versionId", DocumentSchema>(
    "documentCollection",
    { versionId }
  ).post(document);
}

/**
 * Returns list of documents associated with given project.
 *
 * @param versionId - The project version to get documents for.
 * @return The project's documents.
 */
export async function getDocuments(
  versionId: string
): Promise<DocumentSchema[]> {
  return buildRequest<DocumentSchema[], "versionId">("documentCollection", {
    versionId,
  }).get();
}

/**
 * Deletes the given document from the database.
 * User must have edit permissions on the project.
 *
 * @param documentId - The document to be deleted.
 */
export async function deleteDocument(documentId: string): Promise<void> {
  await buildRequest<void, "documentId">("document", {
    documentId,
  }).delete();
}

/**
 * Sets the document to be the user's current document.
 * @param documentId - The document to save.
 */
export async function setCurrentDocument(documentId: string): Promise<void> {
  return buildRequest<void, "documentId">("documentCurrent", {
    documentId,
  }).post();
}

/**
 * Removes the current document affiliated with current user.
 */
export async function clearCurrentDocument(): Promise<void> {
  return buildRequest("documentCurrentClear").delete();
}
