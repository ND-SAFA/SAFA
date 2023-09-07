import { defineStore } from "pinia";

import {
  MemberEntitySchema,
  MembershipSchema,
  MembershipType,
  ProjectSchema,
} from "@/types";
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
    /**
     * List of members and their roles in the current organization.
     */
    orgMembers: [] as MembershipSchema[],
    /**
     * List of members and their roles in the current team.
     */
    teamMembers: [] as MembershipSchema[],
  }),
  actions: {
    /**
     * Returns members of a given type.
     * @param type - The type of members to return.
     * @return The given type of members.
     */
    getMembers(type?: MembershipType): MembershipSchema[] {
      if (type === "TEAM") {
        return this.teamMembers;
      } else if (type === "ORGANIZATION") {
        return this.orgMembers;
      }

      return this.members;
    },
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
      } else if (entity.entityType === "ORGANIZATION") {
        this.orgMembers = [
          ...removeMatches(this.orgMembers, "projectMembershipId", ids),
          ...updatedMembers,
        ];
      } else if (entity.entityType === "TEAM") {
        this.teamMembers = [
          ...removeMatches(this.teamMembers, "projectMembershipId", ids),
          ...updatedMembers,
        ];
      }
    },
    /**
     * Deletes from the current project members.
     *
     * @param deletedMembers - The member ids to delete.
     * @param entity - The entity to remove the members of.
     */
    deleteMembers(deletedMembers: string[], entity: MemberEntitySchema): void {
      if (entity.entityType === "PROJECT") {
        this.members = removeMatches(
          this.members,
          "projectMembershipId",
          deletedMembers
        );

        projectStore.project.members = this.members;
      } else if (entity.entityType === "ORGANIZATION") {
        this.orgMembers = removeMatches(
          this.orgMembers,
          "projectMembershipId",
          deletedMembers
        );
      } else if (entity.entityType === "TEAM") {
        this.teamMembers = removeMatches(
          this.teamMembers,
          "projectMembershipId",
          deletedMembers
        );
      }
    },
  },
});

export default useMembers(pinia);
