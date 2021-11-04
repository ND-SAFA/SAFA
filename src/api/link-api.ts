import { TraceLink } from "@/types/domain/links";
import httpClient from "@/api/http-client";
import { PROJECTS_API_PATH } from "@/api/project-api";
import { Artifact } from "@/types/domain/artifact";

export async function getGeneratedLinks(
  projectId: string
): Promise<TraceLink[]> {
  const url = `${PROJECTS_API_PATH}/${projectId}/links/generated`;
  return httpClient<TraceLink[]>(url, {
    method: "GET",
  });
}

export async function generateLinks(
  sourceArtifacts: Artifact[],
  targetArtifacts: Artifact[]
): Promise<TraceLink[]> {
  const url = `${PROJECTS_API_PATH}/links/generate`;
  const payload = { sourceArtifacts, targetArtifacts };
  return httpClient<TraceLink[]>(url, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function approveLink(traceLinkId: string): Promise<void> {
  const url = `${PROJECTS_API_PATH}/links/${traceLinkId}/approve`;
  return httpClient<void>(url, {
    method: "PUT",
  });
}

export async function declineLink(traceLinkId: string): Promise<void> {
  const url = `${PROJECTS_API_PATH}/links/${traceLinkId}/decline`;
  return httpClient<void>(url, {
    method: "PUT",
  });
}

export async function createLink(
  versionId: string,
  source: string,
  target: string
): Promise<TraceLink> {
  const url = `${PROJECTS_API_PATH}/versions/${versionId}/links/create/${source}/${target}`;
  return httpClient<TraceLink>(url, {
    method: "POST",
  });
}
