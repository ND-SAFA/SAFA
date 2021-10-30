import httpClient from "@/api/http-client";
import { ParseArtifactFileResponse, ParseTraceFileResponse } from "@/types/api";

export const PROJECTS_API_PATH = "projects";

export async function parseArtifactFile(
  artifactType: string,
  file: File
): Promise<ParseArtifactFileResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return httpClient<ParseArtifactFileResponse>(
    `${PROJECTS_API_PATH}/parse/artifacts/${artifactType}`,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

export async function parseTraceFile(
  file: File
): Promise<ParseTraceFileResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return httpClient<ParseTraceFileResponse>(
    `${PROJECTS_API_PATH}/parse/traces`,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}
