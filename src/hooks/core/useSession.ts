import { defineStore } from "pinia";

import { IdentifierModel, ProjectRole, SessionModel } from "@/types";
import { createSession, createUser } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the current user session.
 */
export const useSession = defineStore("session", {
  state() {
    return {
      session: createSession(),
      user: createUser(),
    };
  },
  getters: {
    /**
     * @return Whether there is a current session.
     */
    doesSessionExist(): boolean {
      return this.user.userId !== "";
    },
    /**
     * @return The authenticated user, if one exists.
     * @throws If the token does not exist.
     */
    userEmail(): string {
      return this.user.email || "";
    },
  },
  actions: {
    /**
     * Updates the current session.
     */
    updateSession(session: Partial<SessionModel>) {
      this.session = { ...this.session, ...session };
    },
    /**
     * Clears the current session.
     */
    clearSession() {
      this.session = createSession();
      this.user = createUser();
    },
    /**
     * @return Whether the current user owns this project.
     */
    isOwner(project: IdentifierModel): boolean {
      const member = project.members.find(
        (member) => member.email === this.userEmail
      );

      return !!member && member.role === ProjectRole.OWNER;
    },
    /**
     * @return Whether the current user can administrate this project.
     */
    isAdmin(project: IdentifierModel): boolean {
      const member = project.members.find(
        (member) => member.email === this.userEmail
      );

      return (
        !!member && [ProjectRole.OWNER, ProjectRole.ADMIN].includes(member.role)
      );
    },
    /**
     * @return Whether the current user can edit this project.
     */
    isEditor(project: IdentifierModel): boolean {
      const member = project.members.find(
        (member) => member.email === this.userEmail
      );

      return !!member && member.role !== ProjectRole.VIEWER;
    },
  },
});

export default useSession(pinia);
