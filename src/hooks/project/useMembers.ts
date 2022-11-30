import { defineStore } from "pinia";

import { MembershipModel, ProjectModel } from "@/types";
import { removeMatches } from "@/util";
import { pinia } from "@/plugins";
import projectStore from "./useProject";

/**
 * This module defines the state of the current project's members.
 */
export const useMembers = defineStore("members", {
  state: () => ({
    /**
     * List of members and their roles in the project.
     */
    members: [] as MembershipModel[],
  }),
  getters: {},
  actions: {
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectModel): void {
      this.members = project.members;
    },
    /**
     * Updates the current project members.
     *
     * @param updatedMembers - The updated members.
     */
    updateMembers(updatedMembers: MembershipModel[]): void {
      const ids = updatedMembers.map((member) => member.projectMembershipId);

      this.members = [
        ...removeMatches(this.members, "projectMembershipId", ids),
        ...updatedMembers,
      ];

      projectStore.project.members = this.members;
    },
    /**
     * Deletes from the current project members.
     *
     * @param deletedMembers - The member ids to delete.
     */
    deleteMembers(deletedMembers: string[]): void {
      this.members = removeMatches(
        this.members,
        "projectMembershipId",
        deletedMembers
      );

      projectStore.project.members = this.members;
    },
  },
});

export default useMembers(pinia);
