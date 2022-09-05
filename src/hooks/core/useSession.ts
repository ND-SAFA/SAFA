import { defineStore } from "pinia";
import jwt_decode from "jwt-decode";

import { AuthToken, LocalStorageKeys, SessionModel } from "@/types";
import { createSession } from "@/util";
import { pinia } from "@/plugins";
import logStore from "./useLog";

/**
 * This module defines the state of the current user session.
 */
export const useSession = defineStore("session", {
  state() {
    try {
      return {
        session: JSON.parse(
          localStorage.getItem(LocalStorageKeys.SESSION_TOKEN) || ""
        ),
      };
    } catch (e) {
      return { session: createSession() };
    }
  },
  getters: {
    /**
     * @return Whether there is a current session.
     */
    doesSessionExist(): boolean {
      return this.session.token !== "";
    },
    /**
     * @return The current authorization token if one exists.
     * @throws If the token does not exist.
     */
    getToken(): string {
      const { token } = this.session;

      if (token === "") throw Error("No authorization token exists in store.");

      return token;
    },
    /**
     * @return The decoded authentication token is one exists.
     * @throws If the token does not exist.
     */
    authenticationToken(): AuthToken | undefined {
      try {
        return jwt_decode(this.getToken) as AuthToken;
      } catch (e) {
        return undefined;
      }
    },
    /**
     * @return The authenticated user, if one exists.
     * @throws If the token does not exist.
     */
    userEmail(): string {
      return this.authenticationToken?.sub || "";
    },
    /**
     * @returns Whether the current JWT token is empty or has passed its
     * expiration date.
     * @throws If the token does not exist.
     */
    isTokenExpired(): boolean {
      const expirationTime = (this.authenticationToken?.exp || 0) * 1000;

      return !this.doesSessionExist || Date.now() >= expirationTime;
    },
    /**
     * Checks is a token is in the store and
     */
    async hasAuthorization(): Promise<boolean> {
      if (!this.doesSessionExist) {
        return false;
      } else if (this.isTokenExpired) {
        logStore.onWarning("Your session has expired, please log back in.");
        return false;
      }

      return true;
    },
  },
  actions: {
    /**
     * Updates the current session.
     */
    updateSession(session: Partial<SessionModel>) {
      this.session = { ...this.session, ...session };
      localStorage.setItem(
        LocalStorageKeys.SESSION_TOKEN,
        JSON.stringify(this.session)
      );
    },
    /**
     * Clears the current session.
     */
    clearSession() {
      this.session = createSession();
      localStorage.setItem(
        LocalStorageKeys.SESSION_TOKEN,
        JSON.stringify(this.session)
      );
    },
  },
});

export default useSession(pinia);
