import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import jwt_decode from "jwt-decode";
import type { SessionModel } from "@/types";
import { AuthToken } from "@/types";
import { logModule } from "@/store";
import { createSession } from "@/util";

@Module({ namespaced: true, name: "session" })
/**
 * This module defines the state of the current user session.
 */
export default class SessionModule extends VuexModule {
  /**
   * The current active session, if one exists.
   */
  private session = createSession();

  @Action
  /**
   * Updates the current session object.
   */
  async updateSession(session: Partial<SessionModel>): Promise<void> {
    this.SET_SESSION({ ...this.session, ...session });
  }

  @Action({ rawError: true })
  /**
   * Checks is a token is in the store and
   */
  async hasAuthorization(): Promise<boolean> {
    if (this.isTokenEmpty) {
      return false;
    } else if (this.isTokenExpired) {
      logModule.onWarning("Your session has expired, please log back in.");
      return false;
    }

    return true;
  }

  @Mutation
  /**
   * Sets the current session.
   */
  SET_SESSION(session: SessionModel): void {
    this.session = session;
  }

  /**
   * @return Whether there is a current session.
   */
  get getDoesSessionExist(): boolean {
    return this.session.token !== "";
  }

  /**
   * @return The current authorization token if one exists.
   * @throws If the token does not exist.
   */
  get getToken(): string {
    const token = this.session.token;
    if (token === "") {
      throw Error("No authorization token exists in store.");
    }
    return token;
  }

  /**
   * Returns the decoded authentication token is one exists.
   * @throws If the token does not exist.
   */
  get authenticationToken(): AuthToken | undefined {
    try {
      return jwt_decode(this.getToken) as AuthToken;
    } catch (e) {
      return undefined;
    }
  }

  /**
   * Returns the authenticated user, if one exists.
   * @throws If the token does not exist.
   */
  get userEmail(): string {
    return this.authenticationToken?.sub || "";
  }

  /**
   * @return Whether a valid Authorization token is stored in module
   */
  get isTokenEmpty(): boolean {
    return this.session.token === "";
  }

  /**
   * @returns Whether the current JWT token is empty or has passed its
   * expiration date.
   * @throws If the token does not exist.
   */
  get isTokenExpired(): boolean {
    const expirationTime = (this.authenticationToken?.exp || 0) * 1000;

    return this.isTokenEmpty || Date.now() >= expirationTime;
  }
}
