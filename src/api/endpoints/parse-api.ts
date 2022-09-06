import { ParseArtifactFileModel, ParseTraceFileModel } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api";

/**
 * Parses an artifact file into artifacts.
 *
 * @param artifactType - The type of artifact to parse.
 * @param file - The artifact file to parse.
 * @return The parsed artifact file.
 */
export async function parseArtifactFile(
  artifactType: string,
  file: File
): Promise<ParseArtifactFileModel> {
  const formData = new FormData();

  formData.append("file", file);

  return authHttpClient<ParseArtifactFileModel>(
    fillEndpoint(Endpoint.parseArtifactFile, { artifactType }),
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Parses a trace file into trace links.
 *
 * @param file - The trace file to parse.
 * @return The parsed trace file.
 */
export async function parseTraceFile(file: File): Promise<ParseTraceFileModel> {
  const formData = new FormData();

  formData.append("file", file);

  return authHttpClient<ParseTraceFileModel>(
    Endpoint.parseTraceFile,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}
