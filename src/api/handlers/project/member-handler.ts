import { IOHandlerCallback, MembershipModel, ProjectRole } from "@/types";
import { logStore, membersStore, projectStore } from "@/hooks";
import {
  deleteProjectMember,
  getProjectMembers,
  saveProjectMember,
} from "@/api";

/**
 * Returns the current project's members.
 */
export function handleGetMembers(): Promise<void> {
  return getProjectMembers(projectStore.projectId)
    .then((members) => {
      membersStore.updateMembers(members);
    })
    .catch((e) => {
      logStore.onError(`Unable to get members`);
      logStore.onDevError(e.message);
    });
}

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
    .then((member) => {
      membersStore.updateMembers([...membersStore.members, member]);
      logStore.onSuccess(`Member saved on the project: ${memberEmail}`);
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError(`Unable save member: ${memberEmail}`);
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
  logStore.confirm(
    "Remove User from Project",
    `Are you sure you want to remove ${member.email} from project?`,
    async (isConfirmed: boolean) => {
      if (!isConfirmed) return;

      deleteProjectMember(member)
        .then(() => {
          membersStore.deleteMembers([member.projectMembershipId]);
          logStore.onSuccess(`Deleted a member: ${member.email}`);
        })
        .catch((e) => {
          logStore.onError(`Unable to delete member: ${member.email}`);
          logStore.onDevError(e.message);
        });
    }
  );
}
