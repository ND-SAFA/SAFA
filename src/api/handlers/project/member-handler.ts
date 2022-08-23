import {
  ConfirmationType,
  IOHandlerCallback,
  MembershipModel,
  ProjectRole,
} from "@/types";
import { logStore } from "@/hooks";
import { deleteProjectMember, saveProjectMember } from "@/api";

/**
 * Adds a user to a project and logs the status.
 *
 * @param projectId - The project to add this user to.
 * @param memberEmail - The email of the given user.
 * @param projectRole - The role to set for the given user.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleInviteMember(
  projectId: string,
  memberEmail: string,
  projectRole: ProjectRole,
  { onSuccess, onError }: IOHandlerCallback
): void {
  saveProjectMember(projectId, memberEmail, projectRole)
    .then(() => {
      logStore.onSuccess(`Member added to the project: ${memberEmail}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onSuccess(`Unable to add member: ${memberEmail}`);
      logStore.onDevError(e.message);
      onError?.(e);
    });
}

/**
 * Opens a confirmation modal to delete the given member.
 *
 * @param member - The member to delete.
 */
export function handleDeleteMember(member: MembershipModel): void {
  logStore.$patch({
    confirmation: {
      type: ConfirmationType.INFO,
      title: "Remove User from Project",
      body: `Are you sure you want to remove ${member.email} from project?`,
      statusCallback: async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        await deleteProjectMember(member);
      },
    },
  });
}
