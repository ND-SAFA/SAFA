import { ProjectDocument } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates given document under project specified.
 * @param projectId - The project to create the document under.
 * @param document The document to be created.
 */
export async function createOrUpdateDocument(
  projectId: string,
  document: ProjectDocument
): Promise<ProjectDocument> {
  const url = fillEndpoint(Endpoint.createOrUpdateDocument, {
    projectId,
  });
  return authHttpClient<ProjectDocument>(url, {
    method: "POST",
    body: JSON.stringify(document),
  });
}

/**
 * Returns list of documents associated with given project.
 * @param projectId The UUID of the project whose documents are retrieved.
 */
export async function getProjectDocuments(
  projectId: string
): Promise<ProjectDocument[]> {
  const url = fillEndpoint(Endpoint.getProjectDocuments, {
    projectId,
  });
  return authHttpClient<ProjectDocument[]>(url, {
    method: "GET",
  });
}

/**
 * Deletes the given document from the database. User must have edit
 * permissions on the project.
 * @param document The document to be deleted.
 */
export async function deleteDocument(
  document: ProjectDocument
): Promise<ProjectDocument> {
  const url = fillEndpoint(Endpoint.deleteDocument, {
    documentId: document.documentId,
  });

  await authHttpClient<void>(url, {
    method: "DELETE",
  });

  return document;
}
