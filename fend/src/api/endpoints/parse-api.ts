import { ParseArtifactFileSchema, ParseTraceFileSchema } from "@/types";
import { buildRequest } from "@/api";

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

  return buildRequest<ParseArtifactFileSchema, "artifactType", FormData>(
    "parseArtifacts",
    { artifactType }
  )
    .withFormData()
    .post(formData);
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

  return buildRequest<ParseTraceFileSchema, string, FormData>("parseTraces")
    .withFormData()
    .post(formData);
}
