import {
  MemberRequest,
  Project,
  ProjectCreationResponse,
  ProjectDelta,
  ProjectIdentifier,
  ProjectMembership,
  ProjectRole,
} from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/endpoints/util";

/**
 * Creates a new project from the given flat files.
 *
 * @param formData - Form data containing the project files.
 *
 * @return The created project.
 */
export async function createProjectFromFlatFiles(
  formData: FormData
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(
    Endpoint.createProjectFromFlatFiles,
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param formData - Form data containing the project files.
 *
 * @return The updated project.
 */
export async function updateProjectThroughFlatFiles(
  versionId: string,
  formData: FormData
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(
    fillEndpoint(Endpoint.updateProjectThroughFlatFiles, { versionId }),
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Saves or updates the given project.
 *
 * @param project - The project to save.
 *
 * @return The saved project.
 */
export async function saveOrUpdateProject(
  project: Project
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(Endpoint.project, {
    method: "POST",
    body: JSON.stringify(project),
  });
}

/**
 * Returns all project identifiers.
 *
 * @return All project identifiers.
 */
export async function getProjects(): Promise<ProjectIdentifier[]> {
  return authHttpClient<ProjectIdentifier[]>(Endpoint.project, {
    method: "GET",
  });
}

/**
 * Deletes a project.
 *
 * @param projectId - The project ID to delete.
 */
export async function deleteProject(projectId: string): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.updateProject, { projectId }),
    {
      method: "DELETE",
    }
  );
}

/**
 * Generates the delta between two project versions.
 *
 * @param sourceVersionId - The source version of the project.
 * @param targetVersionId - The target version of the project.
 *
 * @return The delta from the source to the target versions.
 */
export async function getProjectDelta(
  sourceVersionId: string,
  targetVersionId: string
): Promise<ProjectDelta> {
  return authHttpClient<ProjectDelta>(
    fillEndpoint(Endpoint.getProjectDelta, {
      sourceVersionId,
      targetVersionId,
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Returns the list of project members in given project.
 */
export async function getProjectMembers(
  projectId: string
): Promise<ProjectMembership[]> {
  return authHttpClient<ProjectMembership[]>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId,
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Shares project with given user containing email at set role.
 */

export async function addOrUpdateProjectMember(
  projectId: string,
  memberEmail: string,
  projectRole: ProjectRole
): Promise<ProjectMembership[]> {
  const payload: MemberRequest = {
    memberEmail,
    projectRole,
  };
  return authHttpClient<ProjectMembership[]>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}

/**
 * Shares project with given user containing email at set role.
 */

export async function deleteProjectMember(
  projectMember: ProjectMembership
): Promise<ProjectMembership[]> {
  const projectMemberId = projectMember.projectMembershipId;
  return authHttpClient<ProjectMembership[]>(
    fillEndpoint(Endpoint.deleteProjectMember, {
      projectMemberId,
    }),
    {
      method: "DELETE",
    }
  );
}
