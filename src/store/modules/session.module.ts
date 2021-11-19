import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { SessionModel, UserModel } from "@/types";
import { getSession, loginUser, logoutUser } from "@/api";

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
   * Attempts to get an existing session.
   *
   * @throws Error - No session exists.
   */
  async loadSession(): Promise<void> {
    const session = await getSession();

    this.SET_SESSION(session);
  }

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
    await logoutUser();

    this.SET_SESSION(emptySessionModel);
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
  get getToken(): string | undefined {
    const token = this.session.token;
    return token === "" ? undefined : token;
  }
}
