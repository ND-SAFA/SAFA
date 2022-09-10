import {
  CreateProjectByJsonModel,
  IdentifierModel,
  JobModel,
  MemberRequestModel,
  MembershipModel,
  ProjectDelta,
  ProjectModel,
  ProjectRole,
} from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates or updates the given project.
 *
 * @param project - The project to save.
 * @return The saved project.
 */
export async function saveProject(
  project: Pick<ProjectModel, "projectId" | "name" | "description">
): Promise<ProjectModel> {
  return authHttpClient<ProjectModel>(Endpoint.project, {
    method: "POST",
    body: JSON.stringify(project),
  });
}

export async function createProjectCreationJob(
  payload: CreateProjectByJsonModel
): Promise<JobModel> {
  return authHttpClient<JobModel>(Endpoint.createProjectJob, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * Returns all project identifiers.
 *
 * @return All project identifiers.
 */
export async function getProjects(): Promise<IdentifierModel[]> {
  return authHttpClient<IdentifierModel[]>(Endpoint.project, {
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
 * @return The delta from the source to the target versions.
 */
export async function getProjectDelta(
  targetVersionId: string,
  sourceVersionId: string
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
): Promise<MembershipModel[]> {
  return authHttpClient<MembershipModel[]>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId,
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Shares a project with a user.
 *
 * @param projectId - The project to add this user to.
 * @param memberEmail - The email of the given user.
 * @param projectRole - The role to set for the given user.
 */
export async function saveProjectMember(
  projectId: string,
  memberEmail: string,
  projectRole: ProjectRole
): Promise<MembershipModel> {
  return authHttpClient<MembershipModel>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify({
        memberEmail,
        projectRole,
      } as MemberRequestModel),
    }
  );
}

/**
 * Deletes a user from a project.
 *
 * @param projectMember - The user to delete.
 * @return The remaining users.
 */
export async function deleteProjectMember({
  projectMembershipId,
}: MembershipModel): Promise<MembershipModel[]> {
  return authHttpClient<MembershipModel[]>(
    fillEndpoint(Endpoint.deleteProjectMember, {
      projectMemberId: projectMembershipId,
    }),
    {
      method: "DELETE",
    }
  );
}
