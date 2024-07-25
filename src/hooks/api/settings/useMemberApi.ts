import { defineStore } from "pinia";

import { computed } from "vue";
import {
  IdentifierSchema,
  InviteMembershipSchema,
  InviteTokenSchema,
  IOHandlerCallback,
  MemberApiHook,
  MemberEntitySchema,
  MembershipSchema,
  OrganizationSchema,
  TeamSchema,
} from "@/types";
import { buildMember } from "@/util";
import {
  getOrgApiStore,
  getProjectApiStore,
  getVersionApiStore,
  logStore,
  membersStore,
  projectStore,
  sessionStore,
  useApi,
} from "@/hooks";
import {
  acceptInvite,
  createMember,
  deleteMember,
  editMember,
  getMembers,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing member API requests.
 */
export const useMemberApi = defineStore("memberApi", (): MemberApiHook => {
  const memberApi = useApi("memberApi");

  const loading = computed(() => memberApi.loading);

  async function handleReload(entity: MemberEntitySchema): Promise<void> {
    if (!entity.entityId) return;

    await memberApi.handleRequest(
      async () => {
        const members = await getMembers(entity);

        membersStore.updateMembers(members, entity);
      },
      { error: `Unable to get members` }
    );
  }

  async function handleInvite(
    member: InviteMembershipSchema,
    entity: MemberEntitySchema,
    callbacks: IOHandlerCallback<InviteTokenSchema> = {}
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const inviteToken = await createMember(entity.entityId, member);

        membersStore.updateMembers(
          [buildMember({ ...member, ...entity })],
          entity
        );

        if (!member.email) {
          await navigator.clipboard.writeText(inviteToken.url);
        }

        return inviteToken;
      },
      {
        ...callbacks,
        success: member.email
          ? `An invite has been sent to ${member.email}`
          : `Invite link copied to clipboard`,
        error: member.email
          ? `Unable to invite member: ${member.email}`
          : "Unable to create invite link",
      }
    );
  }

  async function handleAcceptInvite(token: string): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const newMember = await acceptInvite(token);

        if (newMember.entityType === "PROJECT") {
          await getVersionApiStore.handleLoadCurrent({
            projectId: newMember.entityId,
          });
        } else if (newMember.entityType === "ORGANIZATION") {
          await getOrgApiStore.handleLoad(newMember.entityId);
        } else if (newMember.entityType === "TEAM") {
          // TODO: navigate to the correct org and team.
          await getOrgApiStore.handleLoadCurrent();
        }
      },
      {
        success: "Successfully accepted invite",
        error: "Unable to accept invite",
      }
    );
  }

  async function handleSaveRole(
    member: MembershipSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const entityId = member.entityId || projectStore.projectId;

        const updatedMember = await editMember({
          ...member,
          entityId,
        });

        membersStore.updateMembers([updatedMember], member);
      },
      {
        ...callbacks,
        success: `Member is now an ${member.role.toLowerCase()}: ${
          member.email
        }`,
        error: `Unable to change member to ${member.role.toLowerCase()}: ${
          member.email
        }`,
      }
    );
  }

  function handleDelete(
    member: MembershipSchema,
    context:
      | IdentifierSchema
      | TeamSchema
      | OrganizationSchema = projectStore.project
  ): void {
    const ownerCount = context.members.filter(
      (member) => member.role === "OWNER"
    ).length;
    const email =
      sessionStore.user?.email === member.email
        ? "yourself"
        : `"${member.email}"`;

    if (member.role === "OWNER" && ownerCount === 1) {
      logStore.onInfo("You cannot remove the only owner of this project.");
      return;
    }

    logStore.confirm(
      "Remove User",
      `Are you sure you want to remove ${email}?`,
      async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        await memberApi.handleRequest(
          async () => {
            await deleteMember(member);
            membersStore.deleteMembers([member.id], member);
            await getProjectApiStore.handleLoadProjects();
          },
          {
            success: `Deleted a member: ${member.email}`,
            error: `Unable to delete member: ${member.email}`,
          }
        );
      }
    );
  }

  return {
    loading,
    handleReload,
    handleInvite,
    handleAcceptInvite,
    handleDelete,
    handleSaveRole,
  };
});

export default useMemberApi(pinia);
