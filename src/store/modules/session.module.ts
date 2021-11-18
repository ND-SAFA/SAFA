import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { SessionModel, UserModel } from "@/types";
import { getSession, loginUser, logoutUser } from "@/api";

/**
 * If you only knew how many things I tried to not have to resort to this...
 */
export let sessionIsLoaded = false;
export let localSession: SessionModel | undefined;

@Module({ namespaced: true, name: "session" })
/**
 * This module defines the state of the current user session.
 */
export default class SessionModule extends VuexModule {
  /**
   * The current active session, if one exists.
   */
  private session?: SessionModel;

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
    console.log("STARTING LOGIN....");
    const session = await loginUser(user);

    console.log("SESSION COMPLETE.", session);
    this.SET_SESSION(session);
    this.session = session;
    console.log("SESSION");
  }

  @Action({ rawError: true })
  /**
   * Attempts to log a user out.
   */
  async logout(): Promise<void> {
    await logoutUser();

    this.SET_SESSION();
  }

  @Mutation
  /**
   * Sets the current session.
   */
  SET_SESSION(session?: SessionModel): void {
    this.session = session;
    localSession = session;
    sessionIsLoaded = !!session;
  }

  /**
   * @return Whether there is a current session.
   */
  get getDoesSessionExist(): boolean {
    return !!this.session;
  }
}
