import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import { SessionModel, UserModel } from "@/types";
import { loginUser } from "@/api";

@Module({ namespaced: true, name: "session" })
/**
 * This module defines the state of the current user session.
 */
export default class SessionModule extends VuexModule {
  /**
   * The current active session, if one exists.
   */
  private session?: SessionModel;

  @Action
  /**
   * Attempts to log a user in.
   *
   * @throws Error - Login failed.
   */
  async login(user: UserModel): Promise<void> {
    const session = await loginUser(user);

    await this.SET_SESSION(session);
  }

  @Mutation
  /**
   * Sets the current session.
   */
  SET_SESSION(session: SessionModel): void {
    this.session = session;
  }

  /**
   * @return Whether there is a current session
   */
  get getDoesSessionExist(): boolean {
    return !!this.session;
  }
}
