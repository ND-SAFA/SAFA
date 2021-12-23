import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { SessionModel, UserModel } from "@/types";
import {
  getCurrentVersion,
  getProjects,
  loginUser,
  loadVersionIfExistsHandler,
} from "@/api";
import { navigateTo, Routes } from "@/router";
import { AuthToken } from "@/types";
import { appModule, deltaModule, projectModule, subtreeModule } from "@/store";
import jwt_decode from "jwt-decode";

/**
 * If you only knew how many things I tried to not have to resort to this...
 */
const emptySessionModel: SessionModel = {
  token: "",
  versionId: "",
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
   * Loads the last stored project.
   */
  async loadLastProject(): Promise<void> {
    const projects = await getProjects();

    if (projects.length) {
      const versionId = (await getCurrentVersion(projects[0].projectId))
        .versionId;

      this.SET_SESSION({ ...this.session, versionId });

      await loadVersionIfExistsHandler(versionId);
    } else {
      await navigateTo(Routes.PROJECT_CREATOR);
    }
  }

  @Action({ rawError: true })
  /**
   * Attempts to log a user out.
   */
  async logout(): Promise<void> {
    this.SET_SESSION(emptySessionModel);

    await navigateTo(Routes.LOGIN_ACCOUNT);
    await projectModule.clearProject();
    deltaModule.clearDelta();
    subtreeModule.clearSubtrees();
  }

  @Action({ rawError: true })
  /**
   * Checks is a token is in the store and
   */
  async hasAuthorization(): Promise<boolean> {
    if (this.isTokenEmpty) {
      return false;
    } else if (this.isTokenExpired) {
      appModule.onWarning("Your session has expired, please log back in.");
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
