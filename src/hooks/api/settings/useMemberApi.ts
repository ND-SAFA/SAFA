import { defineStore } from "pinia";

import { computed } from "vue";
import { Message } from "webstomp-client";
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
  getProjectApiStore,
  logStore,
  membersStore,
  projectStore,
  sessionStore,
  stompApiStore,
  useApi,
} from "@/hooks";
import {
  createMember,
  deleteMember,
  editMember,
  fillEndpoint,
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
    member: MembershipSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const entityId = member.entityId || projectStore.projectId;
        const entityType = member.entityType || "PROJECT";

        const invitedMember = await createMember({
          ...member,
          entityId,
        });

        membersStore.updateMembers(
          [...membersStore.getMembers(entityType), invitedMember],
          member
        );
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
        const entityId = member.entityId || projectStore.projectId;
        const entityType = member.entityType || "PROJECT";

        const updatedMember = await editMember({
          ...member,
          entityId,
        });

        membersStore.updateMembers(
          [
            updatedMember,
            ...removeMatches(
              membersStore.getMembers(entityType),
              "projectMembershipId",
              [updatedMember.projectMembershipId]
            ),
          ],
          member
        );
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
            membersStore.deleteMembers([member.projectMembershipId], member);
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

  async function subscribeToUser(): Promise<void> {
    const userId = sessionStore.userId;
    const topic = fillEndpoint("userTopic", { userId });
    console.log("USER TOPIC:" + topic);
    await stompApiStore.subscribeToStomp(topic, (message: Message) => {
      console.log("USER MESSAGE:" + message.body);
    });
  }

  return {
    loading,
    handleReload,
    handleInvite,
    handleDelete,
    handleSaveRole,
    subscribeToUser,
  };
});

export default useMemberApi(pinia);
