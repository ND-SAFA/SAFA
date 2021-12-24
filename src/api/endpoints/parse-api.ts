import { ParseArtifactFileResponse, ParseTraceFileResponse } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/endpoints/util";

/**
 * Sends BEND an ArtifactDefinition file and returns parsed artifacts and errors.
 *
 * @param artifactType - The type of artifact to parse.
 * @param file - The artifact file to parse.
 *
 * @return The parsed artifact file.
 */
export async function parseArtifactFile(
  artifactType: string,
  file: File
): Promise<ParseArtifactFileResponse> {
  const formData = new FormData();

  formData.append("file", file);

  return authHttpClient<ParseArtifactFileResponse>(
    fillEndpoint(Endpoint.parseArtifactFile, { artifactType }),
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Parses a trace file.
 *
 * @param file - The trace file to parse.
 *
 * @return The parsed trace file.
 */
export async function parseTraceFile(
  file: File
): Promise<ParseTraceFileResponse> {
  const formData = new FormData();

  formData.append("file", file);

  return authHttpClient<ParseTraceFileResponse>(
    Endpoint.parseTraceFile,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}
