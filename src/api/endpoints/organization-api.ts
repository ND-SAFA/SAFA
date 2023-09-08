import {
  MemberEntitySchema,
  MemberRequestSchema,
  MembershipSchema,
  OrganizationSchema,
  TeamSchema,
} from "@/types";
import { buildRequest } from "@/api";

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
export async function getOrganizations(): Promise<OrganizationSchema[]> {
  // TODO
  return [exampleOrg(), exampleOrg(1)];
}

/**
 * Returns the organization with the given id.
 *
 * @param id - The id of the organization to return.
 * @return The organization.
 */
export async function getOrganization(id: string): Promise<OrganizationSchema> {
  // TODO
  return exampleOrg(id);
}

/**
 * Creates a new organization.
 *
 * @param org - The organization to create.
 * @return The created organization.
 */
export async function createOrganization(
  org: Pick<OrganizationSchema, "name" | "description">
): Promise<OrganizationSchema> {
  // TODO
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
  // TODO
  return org;
}

/**
 * Deletes an organization.
 *
 * @param org - The organization to delete.
 */
export async function deleteOrganization(
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  org: OrganizationSchema
): Promise<void> {
  // TODO
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
  // TODO
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
  // TODO
  return team;
}

/**
 * Deletes a team.
 *
 * @param orgId - The organization to delete the team from.
 * @param team - The team to delete.
 */
export async function deleteTeam(
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  orgId: string,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  team: TeamSchema
): Promise<void> {
  // TODO
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
  // TODO
  return buildRequest<MembershipSchema[], "projectId">("getProjectMembers")
    .withParam("projectId", entity.entityId || "")
    .get();
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
  // TODO
  return buildRequest<MembershipSchema, "projectId", MemberRequestSchema>(
    "updateProjectMember"
  )
    .withParam("projectId", member.entityId || "")
    .post({
      memberEmail: member.email,
      projectRole: member.role,
    });
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
  // TODO
  return buildRequest<MembershipSchema, "projectId", MemberRequestSchema>(
    "updateProjectMember"
  )
    .withParam("projectId", member.entityId || "")
    .post({
      memberEmail: member.email,
      projectRole: member.role,
    });
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
  // TODO
  return buildRequest<MembershipSchema, "projectMemberId">(
    "deleteProjectMember"
  )
    .withParam("projectMemberId", member.projectMembershipId)
    .delete();
}
