import { defineStore } from "pinia";

import { MemberEntitySchema, MembershipSchema, MembershipType } from "@/types";
import { removeMatches } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the current project's members.
 */
export const useMembers = defineStore("members", {
  state: () => ({
    /**
     * @return The list of members and their roles in the current project.
     */
    members: [] as MembershipSchema[],
    /**
     * @return The list of members and their roles in the current organization.
     */
    orgMembers: [] as MembershipSchema[],
    /**
     * @return The list of members and their roles in the current team.
     */
    teamMembers: [] as MembershipSchema[],
  }),
  getters: {
    /**
     * @return Active members of the project.
     */
    activeMembers(): MembershipSchema[] {
      return this.members.filter((m) => m.active);
    },
  },
  actions: {
    /**
     * Initializes the members of the current project, team, or org
     * @param members - The members to initialize.
     * @param type - The type of members to initialize.
     */
    initialize(members: MembershipSchema[], type: MembershipType): void {
      if (type === "TEAM") {
        this.teamMembers = members;
      } else if (type === "ORGANIZATION") {
        this.orgMembers = members;
      } else {
        this.members = members;
      }
    },
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
     * Updates which members are active on the current project.
     * @param members - The members to update to active.
     */
    setActiveMembers(members: MembershipSchema[]): void {
      const activeMemberIds = new Set(members.map((m) => m.email));

      this.members.forEach((member) => {
        member.active = activeMemberIds.has(member.email);
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
      const ids = updatedMembers.map((member) => member.id);

      if (entity.entityType === "PROJECT") {
        this.members = [
          ...removeMatches(this.members, "id", ids),
          ...updatedMembers,
        ];
      } else if (entity.entityType === "ORGANIZATION") {
        this.orgMembers = [
          ...removeMatches(this.orgMembers, "id", ids),
          ...updatedMembers,
        ];
      } else if (entity.entityType === "TEAM") {
        this.teamMembers = [
          ...removeMatches(this.teamMembers, "id", ids),
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
        this.members = removeMatches(this.members, "id", deletedMembers);
      } else if (entity.entityType === "ORGANIZATION") {
        this.orgMembers = removeMatches(this.orgMembers, "id", deletedMembers);
      } else if (entity.entityType === "TEAM") {
        this.teamMembers = removeMatches(
          this.teamMembers,
          "id",
          deletedMembers
        );
      }
    },
  },
});

export default useMembers(pinia);
