import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { SessionModel, UserModel } from "@/types";
import { loginUser } from "@/api";
import { navigateTo, Routes } from "@/router";
import { AuthToken } from "@/types";
import { appModule } from "@/store";
import jwt_decode from "jwt-decode";

/**
 * If you only knew how many things I tried to not have to resort to this...
 */
const emptySessionModel: SessionModel = {
  token: "",
};

@Module({ namespaced: true, name: "session" })
/**
 * This module defines the state of the current user session.
 */
export default class SessionModule extends VuexModule {
  /**
   * The current active session, if one exists.
   */
  private session: SessionModel = emptySessionModel;

  @Action({ rawError: true })
  /**
   * Attempts to log a user in.
   *
   * @throws Error - Login failed.
   */
  async login(user: UserModel): Promise<void> {
    const session = await loginUser(user);
    this.SET_SESSION(session);
  }

  @Action({ rawError: true })
  /**
   * Attempts to log a user out.
   */
  async logout(): Promise<void> {
    this.SET_SESSION(emptySessionModel);
    await navigateTo(Routes.LOGIN_ACCOUNT);
  }

  @Action({ rawError: true })
  /**
   * Checks is a token is in the store and
   */
  async hasAuthorization(): Promise<boolean> {
    let error;
    if (this.isTokenEmpty) {
      return false;
    } else if (this.isTokenExpired) {
      error = "Your session has expired, please log back in.";
      appModule.onWarning(error);
      await this.logout();
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
   */
  get authenticationToken(): AuthToken {
    return jwt_decode(this.getToken) as AuthToken;
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
   */
  get isTokenExpired(): boolean {
    return (
      this.isTokenEmpty || Date.now() >= this.authenticationToken.exp * 1000
    );
  }
}
