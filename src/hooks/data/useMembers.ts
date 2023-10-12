import { defineStore } from "pinia";

import { MemberEntitySchema, MembershipSchema, MembershipType } from "@/types";
import { removeMatches } from "@/util";
import { orgStore, projectStore, teamStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the current project's members.
 */
export const useMembers = defineStore("members", {
  getters: {
    /**
     * @return Active members of the project.
     */
    activeMembers(): MembershipSchema[] {
      return projectStore.project.members.filter((m) => m.active);
    },
    /**
     * @return The list of members and their roles in the current project.
     */
    members(): MembershipSchema[] {
      return projectStore.project.members;
    },
    /**
     * @return The list of members and their roles in the current organization.
     */
    orgMembers(): MembershipSchema[] {
      return orgStore.org.members;
    },
    /**
     * @return The list of members and their roles in the current team.
     */
    teamMembers(): MembershipSchema[] {
      return teamStore.team.members;
    },
  },
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
    setActiveMembers(members: MembershipSchema[]): void {
      const activeMemberIds = new Set(members.map((m) => m.email));
      const currentMembers: MembershipSchema[] = projectStore.project.members;
      projectStore.project.members = currentMembers.map((m) => {
        m.active = activeMemberIds.has(m.email);
        return m;
      });
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
        projectStore.project.members = [
          ...removeMatches(this.members, "projectMembershipId", ids),
          ...updatedMembers,
        ];

        projectStore.project.members = this.members;
      } else if (entity.entityType === "ORGANIZATION") {
        orgStore.org.members = [
          ...removeMatches(this.orgMembers, "projectMembershipId", ids),
          ...updatedMembers,
        ];
      } else if (entity.entityType === "TEAM") {
        teamStore.team.members = [
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
        projectStore.project.members = removeMatches(
          this.members,
          "projectMembershipId",
          deletedMembers
        );

        projectStore.project.members = this.members;
      } else if (entity.entityType === "ORGANIZATION") {
        orgStore.org.members = removeMatches(
          this.orgMembers,
          "projectMembershipId",
          deletedMembers
        );
      } else if (entity.entityType === "TEAM") {
        teamStore.team.members = removeMatches(
          this.teamMembers,
          "projectMembershipId",
          deletedMembers
        );
      }
    },
  },
});

export default useMembers(pinia);
