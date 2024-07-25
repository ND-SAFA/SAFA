import {
  InviteMembershipSchema,
  InviteTokenSchema,
  MemberEntitySchema,
  MembershipSchema,
} from "@/types";
import { buildRequest } from "@/api";

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
 * If an email is provided, an invite email will be sent.
 * Otherwise, a general share link will be copied to the clipboard.
 *
 * @param entityId - The id of the entity to add the member to.
 * @param member - The member to add.
 * @return The created member.
 */
export async function createMember(
  entityId: string,
  member: InviteMembershipSchema
): Promise<InviteTokenSchema> {
  return buildRequest<InviteTokenSchema, "entityId", InviteMembershipSchema>(
    "memberInvite",
    { entityId }
  ).post(member);
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

/**
 * Accepts an invite to join a project, team, or organization.
 * @param token - The invite token.
 * @return The accepted membership.
 */
export function acceptInvite(token: string): Promise<MembershipSchema> {
  return buildRequest<MembershipSchema, string>(
    "memberInviteAccept",
    {},
    { token }
  ).put();
}

/**
 * Declines an invite to join a project, team, or organization.
 * @param token - The invite token.
 */
export function declineInvite(token: string): Promise<void> {
  return buildRequest<void, string>("memberInviteDecline", {}, { token }).put();
}
