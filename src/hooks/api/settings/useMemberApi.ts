import { defineStore } from "pinia";

import { computed } from "vue";
import {
  IdentifierSchema,
  IOHandlerCallback,
  MemberApiHook,
  MemberEntitySchema,
  MembershipSchema,
  OrganizationSchema,
  TeamSchema,
} from "@/types";
import { removeMatches } from "@/util";
import {
  useApi,
  getProjectApiStore,
  logStore,
  membersStore,
  sessionStore,
  projectStore,
} from "@/hooks";
import { deleteMember, editMember, createMember, getMembers } from "@/api";
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
    member: MembershipSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        if (member.entityType === "PROJECT") {
          const invitedMember = await createMember({
            ...member,
            entityId: projectStore.projectId,
          });

          membersStore.updateMembers(
            [...membersStore.members, invitedMember],
            member
          );
        }
      },
      {
        ...callbacks,
        success: `Member has been added: ${member.email}`,
        error: `Unable save member: ${member.email}`,
      }
    );
  }

  async function handleSaveRole(
    member: MembershipSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        if (member.entityType === "PROJECT") {
          const updatedMember = await editMember({
            ...member,
            entityId: projectStore.projectId,
          });

          membersStore.updateMembers(
            [
              updatedMember,
              ...removeMatches(membersStore.members, "projectMembershipId", [
                updatedMember.projectMembershipId,
              ]),
            ],
            member
          );
        }
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

    if (member.entityType === "PROJECT") {
      logStore.confirm(
        "Remove User from Project",
        `Are you sure you want to remove ${email} from this project?`,
        async (isConfirmed: boolean) => {
          if (!isConfirmed) return;

          await memberApi.handleRequest(
            async () => {
              await deleteMember(member);
              membersStore.deleteMembers([member.projectMembershipId]);
              await getProjectApiStore.handleReload();
            },
            {
              success: `Deleted a member: ${member.email}`,
              error: `Unable to delete member: ${member.email}`,
            }
          );
        }
      );
    }
  }

  return {
    loading,
    handleReload,
    handleInvite,
    handleDelete,
    handleSaveRole,
  };
});

export default useMemberApi(pinia);
