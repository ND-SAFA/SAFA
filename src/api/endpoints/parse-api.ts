import { ParseArtifactFileSchema, ParseTraceFileSchema } from "@/types";
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
): Promise<ParseArtifactFileSchema> {
  const formData = new FormData();

  formData.append("file", file);

  return authHttpClient<ParseArtifactFileSchema>(
    fillEndpoint(Endpoint.parseArtifactFile, { artifactType }),
    {
      method: "POST",
      body: formData,
    },
    { setJsonContentType: false }
  );
}

/**
 * Parses a trace file into trace links.
 *
 * @param file - The trace file to parse.
 * @return The parsed trace file.
 */
export async function parseTraceFile(
  file: File
): Promise<ParseTraceFileSchema> {
  const formData = new FormData();

  formData.append("file", file);

  return authHttpClient<ParseTraceFileSchema>(
    Endpoint.parseTraceFile,
    {
      method: "POST",
      body: formData,
    },
    { setJsonContentType: false }
  );
}
