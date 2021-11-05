import { PROJECTS_API_PATH } from "@/api/project-api";
import { ArtifactNameValidationResponse } from "@/types";
import { Artifact } from "@/types";
import httpClient from "@/api/http-client";

export async function isArtifactNameTaken(
  projectId: string,
  artifactName: string
): Promise<ArtifactNameValidationResponse> {
  const url = `${PROJECTS_API_PATH}/${projectId}/artifacts/validate/${artifactName}`;
  return httpClient<ArtifactNameValidationResponse>(url, {
    method: "GET",
  });
}

export async function createNewArtifact(
  versionId: string,
  artifact: Artifact
): Promise<Artifact> {
  return httpClient<Artifact>(
    `${PROJECTS_API_PATH}/versions/${versionId}/artifacts`,
    {
      method: "POST",
      body: JSON.stringify(artifact),
    }
  );
}
