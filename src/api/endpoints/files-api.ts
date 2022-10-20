import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Downloads project files for the given version.
 * @param versionId - The version to download.
 * @param fileType - The file format to download.
 */
export async function getProjectFiles(
  versionId: string,
  fileType: "csv" | "json" = "csv"
): Promise<string> {
  return authHttpClient<string>(
    fillEndpoint(Endpoint.getProjectFiles, { versionId, fileType }),
    {
      method: "GET",
    },
    { arrayBuffer: true }
  );
}
