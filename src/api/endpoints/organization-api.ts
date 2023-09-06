import {
  MemberEntitySchema,
  MemberRequestSchema,
  MembershipSchema,
  OrganizationSchema,
  TeamSchema,
} from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

const exampleMember = (id: string | number = 0): MembershipSchema => ({
  projectMembershipId: id.toString(),
  email: `${id}@example.com`,
  role: "VIEWER",
});

const exampleTeam = (id: string | number = 0): TeamSchema => ({
  id: id.toString(),
  name: `Team ${id}`,
  members: [exampleMember(), exampleMember(1)],
  projects: [],
});

const exampleOrg = (id: string | number = 0): OrganizationSchema => ({
  id: id.toString(),
  name: `Organization ${id}`,
  description: "An example description",
  members: [exampleMember(), exampleMember(1)],
  personalOrg: id === 0,
  paymentTier: "FREE",
  teams: [exampleTeam(), exampleTeam(1)],
});

/**
 * Returns all organizations for the current user.
 *
 * @return All organizations.
 */
export async function getAllOrganizations(): Promise<OrganizationSchema[]> {
  return [exampleOrg(), exampleOrg(1)];
}

/**
 * Returns the organization with the given id.
 *
 * @param id - The id of the organization to return.
 * @return The organization.
 */
export async function getOrganization(id: string): Promise<OrganizationSchema> {
  return exampleOrg(id);
}

/**
 * Creates a new organization.
 *
 * @param org - The organization to create.
 * @return The created organization.
 */
export async function createOrganization(
  org: Omit<OrganizationSchema, "id">
): Promise<OrganizationSchema> {
  return {
    ...exampleOrg(),
    ...org,
  };
}

/**
 * Edits an organization.
 *
 * @param org - The organization to edit.
 * @return The edited organization.
 */
export async function editOrganization(
  org: OrganizationSchema
): Promise<OrganizationSchema> {
  return org;
}

/**
 * Deletes an organization.
 *
 * @param org - The organization to delete.
 */
export async function deleteOrganization(
  org: OrganizationSchema
): Promise<void> {
  return;
}

/**
 * Creates a new team.
 *
 * @param orgId - The organization to create the team within.
 * @param team - The team to create.
 * @return The created team.
 */
export async function createTeam(
  orgId: string,
  team: Omit<TeamSchema, "id">
): Promise<TeamSchema> {
  return {
    ...exampleTeam(),
    ...team,
  };
}

/**
 * Edits a team.
 *
 * @param orgId - The organization to edit the team within.
 * @param team - The team to edit.
 * @return The edited team.
 */
export async function editTeam(
  orgId: string,
  team: TeamSchema
): Promise<TeamSchema> {
  return team;
}

/**
 * Deletes a team.
 *
 * @param orgId - The organization to delete the team from.
 * @param team - The team to delete.
 */
export async function deleteTeam(
  orgId: string,
  team: TeamSchema
): Promise<void> {
  return;
}

/**
 * Get the members of a project, team, or organization.
 *
 * @param entity - The entity to get the members of.
 * @return The members of the entity.
 */
export async function getMembers(
  entity: MemberEntitySchema
): Promise<MembershipSchema[]> {
  return authHttpClient<MembershipSchema[]>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId: entity.entityId || "",
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Shares a project, team, or organization with a user.
 *
 * @param member - The member to add.
 * @return The created member.
 */
export async function createMember(
  member: Omit<MembershipSchema, "projectMembershipId">
): Promise<MembershipSchema> {
  return authHttpClient<MembershipSchema>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId: member.entityId || "",
    }),
    {
      method: "POST",
      body: JSON.stringify({
        memberEmail: member.email,
        projectRole: member.role,
      } as MemberRequestSchema),
    }
  );
}

/**
 * Edits a member of a project, team, or organization.
 *
 * @param member - The member to edit.
 * @return The edited member.
 */
export async function editMember(
  member: MembershipSchema
): Promise<MembershipSchema> {
  return authHttpClient<MembershipSchema>(
    fillEndpoint(Endpoint.getProjectMembers, {
      projectId: member.entityId || "",
    }),
    {
      method: "POST",
      body: JSON.stringify({
        memberEmail: member.email,
        projectRole: member.role,
      } as MemberRequestSchema),
    }
  );
}

/**
 * Deletes a member of a project, team, or organization.
 *
 * @param member - The member to delete.
 * @return The delete member.
 */
export async function deleteMember(
  member: MembershipSchema
): Promise<MembershipSchema> {
  return authHttpClient<MembershipSchema>(
    fillEndpoint(Endpoint.deleteProjectMember, {
      projectMemberId: member.projectMembershipId,
    }),
    {
      method: "DELETE",
    }
  );
}
