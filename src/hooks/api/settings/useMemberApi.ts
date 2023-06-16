import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, MembershipSchema, ProjectRole } from "@/types";
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

export const useMemberApi = defineStore("memberApi", () => {
  const memberApi = useApi("memberApi");

  const loading = computed(() => memberApi.loading);

  /**
   * Returns the current project's members.
   */
  async function handleGetMembers(): Promise<void> {
    await memberApi.handleRequest(
      async () => {
        const members = await getProjectMembers(projectStore.projectId);

        membersStore.updateMembers(members);
      },
      {},
      { error: `Unable to get members` }
    );
  }

  /**
   * Adds a user to a project and logs the status.
   *
   * @param projectId - The project to add this user to.
   * @param memberEmail - The email of the given user.
   * @param projectRole - The role to set for the given user.
   * @param callbacks - Callbacks for the request.
   */
  async function handleInviteMember(
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
      callbacks,
      {
        success: `Member has been added: ${memberEmail}`,
        error: `Unable save member: ${memberEmail}`,
      }
    );
  }

  /**
   * Opens a confirmation modal to delete the given member.
   *
   * @param member - The member to delete.
   */
  function handleDeleteMember(member: MembershipSchema): void {
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
            await getProjectApiStore.handleGetProjects({});
          },
          {},
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
    handleGetMembers,
    handleInviteMember,
    handleDeleteMember,
  };
});

export default useMemberApi(pinia);
