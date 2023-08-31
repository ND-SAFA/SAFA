import { defineStore } from "pinia";

import { computed } from "vue";
import {
  IOHandlerCallback,
  MemberApiHook,
  MembershipSchema,
  ProjectRole,
} from "@/types";
import { removeMatches } from "@/util";
import {
  useApi,
  getProjectApiStore,
  logStore,
  membersStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import {
  deleteProjectMember,
  getProjectMembers,
  saveProjectMember,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing member API requests.
 */
export const useMemberApi = defineStore("memberApi", (): MemberApiHook => {
  const memberApi = useApi("memberApi");

  const loading = computed(() => memberApi.loading);

  async function handleReload(): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const members = await getProjectMembers(projectStore.projectId);

        membersStore.updateMembers(members);
      },
      { error: `Unable to get members` }
    );
  }

  async function handleInvite(
    projectId: string,
    memberEmail: string,
    projectRole: ProjectRole,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const member = await saveProjectMember(
          projectId,
          memberEmail,
          projectRole
        );

        membersStore.updateMembers([...membersStore.members, member]);
      },
      {
        ...callbacks,
        success: `Member has been added: ${memberEmail}`,
        error: `Unable save member: ${memberEmail}`,
      }
    );
  }

  async function handleSaveRole(
    projectId: string,
    memberEmail: string,
    projectRole: ProjectRole,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const member = await saveProjectMember(
          projectId,
          memberEmail,
          projectRole
        );

        membersStore.updateMembers([
          member,
          ...removeMatches(membersStore.members, "projectMembershipId", [
            member.projectMembershipId,
          ]),
        ]);
      },
      {
        ...callbacks,
        success: `Member is now an ${projectRole}: ${memberEmail}`,
        error: `Unable to change member to ${projectRole}: ${memberEmail}`,
      }
    );
  }

  function handleDelete(member: MembershipSchema): void {
    const email =
      sessionStore.user?.email === member.email
        ? "yourself"
        : `"${member.email}"`;

    logStore.confirm(
      "Remove User from Project",
      `Are you sure you want to remove ${email} from this project?`,
      async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        await memberApi.handleRequest(
          async () => {
            await deleteProjectMember(member);
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

  return {
    loading,
    handleReload,
    handleInvite,
    handleDelete,
    handleSaveRole,
  };
});

export default useMemberApi(pinia);
