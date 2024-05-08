import {
  MemberEntitySchema,
  MembershipSchema,
  OrganizationSchema,
  TeamSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Returns the user's personal organization.
 *
 * @return The user's organization.
 */
export async function getPersonalOrganization(): Promise<OrganizationSchema> {
  return buildRequest<OrganizationSchema>("organizationSelf").get();
}

/**
 * Returns all organizations for the current user.
 *
 * @return All organizations.
 */
export async function getOrganizations(): Promise<OrganizationSchema[]> {
  return buildRequest<OrganizationSchema[]>("organizationCollection").get();
}

/**
 * Returns the organization with the given id.
 *
 * @param orgId - The id of the organization to return.
 * @return The organization.
 */
export async function getOrganization(
  orgId: string
): Promise<OrganizationSchema> {
  return buildRequest<OrganizationSchema, "orgId">("organization", {
    orgId,
  }).get();
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
  return buildRequest<
    OrganizationSchema,
    string,
    Pick<OrganizationSchema, "name" | "description">
  >("organizationCollection").post(org);
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
  return buildRequest<OrganizationSchema, "orgId", OrganizationSchema>(
    "organization",
    { orgId: org.id }
  ).put(org);
}

/**
 * Deletes an organization.
 *
 * @param org - The organization to delete.
 */
export async function deleteOrganization(
  org: OrganizationSchema
): Promise<void> {
  await buildRequest<OrganizationSchema, "orgId">("organization", {
    orgId: org.id,
  }).delete();
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
  return buildRequest<TeamSchema, "orgId", Omit<TeamSchema, "id">>(
    "teamCollection",
    { orgId }
  ).post(team);
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
  return buildRequest<TeamSchema, "orgId" | "teamId", TeamSchema>("team", {
    orgId,
    teamId: team.id,
  }).put(team);
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
  await buildRequest<TeamSchema, "orgId" | "teamId">("team", {
    orgId,
    teamId: team.id,
  }).delete();
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
  return buildRequest<MembershipSchema[], "entityId">("memberCollection", {
    entityId: entity.entityId || "",
  }).get();
}

/**
 * Shares a project, team, or organization with a user.
 *
 * @param member - The member to add.
 * @return The created member.
 */
export async function createMember(
  member: Omit<MembershipSchema, "id">
): Promise<MembershipSchema> {
  return buildRequest<
    MembershipSchema,
    "entityId",
    Pick<MembershipSchema, "email" | "role">
  >("memberCollection", { entityId: member.entityId || "" }).post({
    email: member.email,
    role: member.role,
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
  return buildRequest<
    MembershipSchema,
    "entityId" | "memberId",
    MembershipSchema
  >("member", { entityId: member.entityId || "", memberId: member.id }).put(
    member
  );
}

/**
 * Deletes a member of a project, team, or organization.
 *
 * @param member - The member to delete.
 * @return The delete member.
 */
export async function deleteMember(member: MembershipSchema): Promise<void> {
  await buildRequest<MembershipSchema, "entityId" | "memberId">("member", {
    entityId: member.entityId || "",
    memberId: member.id,
  }).delete();
}
