import { GeneratedLayoutsModel, LayoutRegenerationModel } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Regenerates layouts for a version & document.
 *
 * @param versionId - The version to generate layouts for.
 * @param documentId - The document to generate layouts for. If empty, the default document will be regenerated.
 * @return The generated layouts.
 */
export async function createLayout(
  versionId: string,
  documentId: string
): Promise<GeneratedLayoutsModel> {
  const body: LayoutRegenerationModel = documentId
    ? { defaultDocument: false, documentIds: [documentId] }
    : { defaultDocument: true, documentIds: [] };

  return authHttpClient<GeneratedLayoutsModel>(
    fillEndpoint(Endpoint.refreshLayout, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(body),
    }
  );
}
