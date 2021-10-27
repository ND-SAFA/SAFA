import { ProjectCreationResponse } from "@/types/api";
import {
  Project,
  ProjectIdentifier,
  ProjectVersion,
} from "@/types/domain/project";
import { DeltaPayload } from "@/types/store";
import httpClient from "@/api/http-client";

export const PROJECTS_API_PATH = "projects";

export async function createProjectFromFlatFiles(
  formData: FormData
): Promise<ProjectCreationResponse> {
  return httpClient<ProjectCreationResponse>(
    `${PROJECTS_API_PATH}/flat-files`,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

export async function updateProjectThroughFlatFiles(
  versionId: string,
  formData: FormData
): Promise<ProjectCreationResponse> {
  return httpClient<ProjectCreationResponse>(
    `${PROJECTS_API_PATH}/versions/${versionId}/flat-files`,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

export async function saveOrUpdateProject(
  project: Project
): Promise<ProjectCreationResponse> {
  return httpClient<ProjectCreationResponse>(`${PROJECTS_API_PATH}`, {
    method: "POST",
    body: JSON.stringify(project),
  });
}

export async function getProjects(): Promise<ProjectIdentifier[]> {
  const url = `${PROJECTS_API_PATH}`;
  return httpClient<ProjectIdentifier[]>(url, {
    method: "GET",
  });
}

export async function getProjectVersion(
  versionId: string
): Promise<ProjectCreationResponse> {
  const url = `${PROJECTS_API_PATH}/versions/${versionId}`;
  return httpClient<ProjectCreationResponse>(url, {
    method: "GET",
  });
}

export async function deleteProject(projectId: string): Promise<void> {
  const url = `${PROJECTS_API_PATH}/${projectId}`;
  return httpClient<void>(url, {
    method: "DELETE",
  });
}

export async function getProjectVersions(
  projectId: string
): Promise<ProjectVersion[]> {
  if (projectId === undefined || projectId === "") {
    throw Error("Undefined project identifier");
  }
  const url = `${PROJECTS_API_PATH}/${projectId}/versions`;
  return httpClient<ProjectVersion[]>(url, {
    method: "GET",
  });
}

export async function getCurrentVersion(
  projectId: string
): Promise<ProjectVersion> {
  if (projectId === undefined || projectId === "") {
    throw Error("Undefined project identifier");
  }
  const url = `${PROJECTS_API_PATH}/${projectId}/versions/current`;
  return httpClient<ProjectVersion>(url, {
    method: "GET",
  });
}

export async function createNewMajorVersion(
  projectId: string
): Promise<ProjectVersion> {
  const url = `${PROJECTS_API_PATH}/${projectId}/versions/major`;
  return httpClient<ProjectVersion>(url, {
    method: "POST",
  });
}

export async function createNewMinorVersion(
  projectId: string
): Promise<ProjectVersion> {
  const url = `${PROJECTS_API_PATH}/${projectId}/versions/minor`;
  return httpClient<ProjectVersion>(url, {
    method: "POST",
  });
}

export async function createNewRevisionVersion(
  projectId: string
): Promise<ProjectVersion> {
  const url = `${PROJECTS_API_PATH}/${projectId}/versions/revision`;
  return httpClient<ProjectVersion>(url, {
    method: "POST",
  });
}

export async function deleteProjectVersion(versionId: string): Promise<void> {
  const url = `${PROJECTS_API_PATH}/versions/${versionId}`;
  return httpClient<void>(url, {
    method: "DELETE",
  });
}

export async function getProjectDelta(
  sourceVersionId: string,
  targetVersionId: string
): Promise<DeltaPayload> {
  const url = `${PROJECTS_API_PATH}/delta/${sourceVersionId}/${targetVersionId}`;
  return httpClient<DeltaPayload>(url, {
    method: "GET",
  });
}
