import { GeneratedLayoutsSchema, LayoutRegenerationSchema } from "@/types";
import { buildRequest } from "@/api";

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
): Promise<GeneratedLayoutsSchema> {
  const body: LayoutRegenerationSchema = documentId
    ? { defaultDocument: false, documentIds: [documentId] }
    : { defaultDocument: true, documentIds: [] };

  return buildRequest<
    GeneratedLayoutsSchema,
    "versionId",
    LayoutRegenerationSchema
  >("layout", { versionId }).post(body);
}
