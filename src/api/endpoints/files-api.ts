import { buildRequest } from "@/api";

/**
 * Downloads project files for the given version.
 * @param versionId - The version to download.
 * @param fileType - The file format to download.
 */
export async function getProjectFiles(
  versionId: string,
  fileType: "csv" | "json" = "csv"
): Promise<string> {
  return buildRequest<string, "versionId" | "fileType">("getProjectFiles")
    .withParam("versionId", versionId)
    .withParam("fileType", fileType)
    .withResponseType("arraybuffer")
    .get();
}
