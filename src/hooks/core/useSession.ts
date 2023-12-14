import { defineStore } from "pinia";

import {
  IdentifierSchema,
  MembershipSchema,
  OrganizationSchema,
  SessionSchema,
  TeamSchema,
  UserSchema,
} from "@/types";
import { buildSession, buildUser } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the current user session.
 */
export const useSession = defineStore("session", {
  state() {
    return {
      /**
       * The current session.
       */
      session: buildSession(),
      /**
       * The current user.
       */
      user: buildUser(),
    };
  },
  getters: {
    /**
     * @return The current user's authentication token.
     */
    authToken(): string {
      return this.session.token;
    },
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
    /**
     * @return The current user's id.
     */
    userId(): string {
      return this.user.userId || "";
    },
  },
  actions: {
    /**
     * Updates the current session.
     */
    updateSession(session: Partial<SessionSchema>) {
      this.session = { ...this.session, ...session };
    },
    /**
     * Updates the current user.
     */
    updateUser(user: Partial<UserSchema>) {
      this.user = { ...this.user, ...user };
    },
    /**
     * Clears the current session.
     */
    clearSession() {
      this.session = buildSession();
      this.user = buildUser();
    },
    /**
     * @return This user's membership within a project, team, or organization.
     */
    getCurrentMember(
      context: IdentifierSchema | TeamSchema | OrganizationSchema
    ): MembershipSchema | undefined {
      return context.members.find((member) => member.email === this.userEmail);
    },
  },
});

export default useSession(pinia);
