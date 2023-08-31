import { defineStore } from "pinia";

import { MemberEntitySchema, MembershipSchema, ProjectSchema } from "@/types";
import { removeMatches } from "@/util";
import { pinia } from "@/plugins";
import projectStore from "./useProject";

/**
 * This module defines the state of the current project's members.
 */
export const useMembers = defineStore("members", {
  state: () => ({
    /**
     * List of members and their roles in the current project.
     */
    members: [] as MembershipSchema[],
  }),
  getters: {},
  actions: {
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectSchema): void {
      this.members = project.members;
    },
    /**
     * Updates the current project members.
     *
     * @param updatedMembers - The updated members.
     * @param entity - The entity to store the members of.
     */
    updateMembers(
      updatedMembers: MembershipSchema[],
      entity: MemberEntitySchema
    ): void {
      const ids = updatedMembers.map((member) => member.projectMembershipId);

      if (entity.entityType === "PROJECT") {
        this.members = [
          ...removeMatches(this.members, "projectMembershipId", ids),
          ...updatedMembers,
        ];

        projectStore.project.members = this.members;
      }
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
