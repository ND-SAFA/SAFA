import { Module, VuexModule } from "vuex-module-decorators";

@Module({ namespaced: true, name: "session" })
/**
 * This module defines the state of the current user session.
 */
export default class SessionModule extends VuexModule {
  /**
   * Whether there is currently an active session.
   */
  private doesSessionExist = false;

  /**
   * @return Whether there is a current session
   */
  get getDoesSessionExist(): boolean {
    return this.doesSessionExist;
  }
}
