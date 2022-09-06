import { ArtifactModel, DocumentModel } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates or updates given document under project specified.
 *
 * @param versionId - The version to mark the document as created.
 * @param document - The document to be created.
 * @return The saved document.
 */
export async function saveDocument(
  versionId: string,
  document: DocumentModel
): Promise<DocumentModel> {
  return authHttpClient<DocumentModel>(
    fillEndpoint(Endpoint.createOrUpdateDocument, {
      versionId,
    }),
    {
      method: "POST",
      body: JSON.stringify(document),
    }
  );
}

/**
 * Returns list of documents associated with given project.
 *
 * @param versionId - The project version to get documents for.
 * @return The project's documents.
 */
export async function getDocuments(
  versionId: string
): Promise<DocumentModel[]> {
  return authHttpClient<DocumentModel[]>(
    fillEndpoint(Endpoint.getProjectDocuments, {
      versionId,
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Deletes the given document from the database.
 * User must have edit permissions on the project.
 *
 * @param document - The document to be deleted.
 */
export async function deleteDocument(document: DocumentModel): Promise<void> {
  await authHttpClient<void>(
    fillEndpoint(Endpoint.deleteDocument, {
      documentId: document.documentId,
    }),
    {
      method: "DELETE",
    }
  );
}

/**
 * Attaches artifacts to a document.
 *
 * @param versionId - The version to mark the addition to.
 * @param documentId - The document to which the artifacts are added to.
 * @param artifacts - The artifacts being added to the document.
 * @return The attached artifacts.
 */
export async function saveDocumentArtifacts(
  versionId: string,
  documentId: string,
  artifacts: ArtifactModel[]
): Promise<ArtifactModel[]> {
  return authHttpClient<ArtifactModel[]>(
    fillEndpoint(Endpoint.addArtifactsToDocument, {
      versionId,
      documentId,
    }),
    {
      method: "POST",
      body: JSON.stringify(artifacts),
    }
  );
}

/**
 * Removed artifacts from a document.
 *
 * @param versionId - The version to mark the removal at.
 * @param documentId - The document to remove the artifacts from.
 * @param artifactId - The artifact to remove from the document.
 */
export async function deleteDocumentArtifact(
  versionId: string,
  documentId: string,
  artifactId: string
): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.removeArtifactFromDocument, {
      versionId,
      documentId,
      artifactId,
    }),
    {
      method: "DELETE",
    }
  );
}

/**
 * Sets the document to be the user's current document.
 * @param documentId The document to save.
 */
export async function setCurrentDocument(documentId: string): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.setCurrentDocument, {
      documentId,
    }),
    {
      method: "POST",
    }
  );
}

/**
 * Removes the current document affiliated with current user.
 */
export async function clearCurrentDocument(): Promise<void> {
  return authHttpClient<void>(fillEndpoint(Endpoint.clearCurrentDocument, {}), {
    method: "DELETE",
  });
}
